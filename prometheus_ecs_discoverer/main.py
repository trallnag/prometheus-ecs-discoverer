"""
Entry to PromED. Contains a lot of instrumentation and is responsible for
looping the discovery. It daemonizes the functionality.
"""

import sys
import time
from timeit import default_timer

import boto3
from botocore.config import Config
from loguru import logger
from prometheus_client import Histogram, start_http_server

from prometheus_ecs_discoverer import discovery, fetching, marshalling, s, telemetry

INTERVAL_BREACHED_COUNTER = telemetry.counter(
    "execution_breaches_total",
    "Number of times the discovery round took longer than the configured interval.",
)
INTERVAL_BREACHED_COUNTER.inc(0)


def configure_logging() -> None:
    """Configure Loguru logging."""

    logger.remove()

    if s.LOG_JSON:
        fmt = "{message}"
        logger.add(sys.stderr, format=fmt, serialize=True, level=s.LOG_LEVEL)
    else:
        fmt = "<green>{time:HH:mm:ss}</green> <level>{level}</level> <cyan>{function}</cyan> {message} <dim>{extra}</dim>"
        logger.add(sys.stderr, colorize=True, format=fmt, level=s.LOG_LEVEL)

    if s.BOTO3_DEBUG:
        import boto3

        boto3.set_stream_logger(name="botocore")


def expose_info() -> None:
    """Expose a gauge with info label values."""

    telemetry.info(
        {
            "interval_seconds": str(s.INTERVAL),
        }
    )

    INTERVAL_INFO = telemetry.gauge(
        "info_interval_seconds", "Configured interval in seconds."
    )
    INTERVAL_INFO.set(s.INTERVAL)


def get_interval_histogram(interval: int) -> Histogram:
    """Create histogram with buckets that fit the given interval.

    10 buckets below the interval and two buckets with 10 second steps larger
    than the interval.

    Args:
        interval (int): Interval PromED is running at.

    Returns:
        Histogram: Prometheus Histogram object.
    """

    steps = 10
    step_size = round(interval / steps, 0)
    return telemetry.histogram(
        "round_duration_seconds",
        "Histogram for duration",
        buckets=tuple(
            [x * step_size for x in range(steps)]
            + [
                interval + 10,
                interval + 20,
                float("inf"),
            ]
        ),
    )


def main():
    interval: int = s.INTERVAL
    output_dir: str = s.OUTPUT_DIRECTORY
    should_throttle: bool = s.WARMUP_THROTTLE

    configure_logging()
    expose_info()

    logger.info("Welcome to PromED, the Prometheus ECS Discoverer.")
    logger.bind(settings=s.as_dict()).info("Here is the used configuration.")

    DURATION_HISTOGRAM = get_interval_histogram(interval)

    if s.PROMETHEUS_START_HTTP_SERVER:
        port = s.PROMETHEUS_SERVER_PORT
        logger.bind(port=port).info("Start Prometheus HTTP server to expose metrics.")
        start_http_server(port=port)

    logger.info("Create Boto3 session.")
    session = boto3.Session()
    config = Config(retries={"max_attempts": s.MAX_RETRY_ATTEMPTS, "mode": "standard"})

    logger.info("Create Boto3 clients and CachedFetcher.")
    fetcher = fetching.CachedFetcher(
        session.client("ecs", config=config),
        session.client("ec2", config=config),
        should_throttle=should_throttle,
        throttle_interval_seconds=s.THROTTLE_INTERVAL_SECONDS,
    )

    logger.info("Create PrometheusEcsDiscoverer.")
    discoverer = discovery.PrometheusEcsDiscoverer(fetcher)

    if should_throttle:
        logger.info("First discovery round will be throttled down.")

    logger.info("Ready for discovery. The discoverer will run until interrupted.")

    first_round = True
    while True:
        logger.info("Start new discovery round.")

        start_time = default_timer()

        if not first_round:
            discoverer.fetcher.should_throttle = False

        targets = discoverer.discover()
        marshalling.write_targets_to_file(targets, output_dir)

        if first_round and should_throttle:
            fetcher.should_throttle = False
            first_round = False

        duration = max(default_timer() - start_time, 0)

        logger.bind(duration=duration).info("Finished discovery round.")
        DURATION_HISTOGRAM.observe(duration)

        if duration > interval:
            logger.bind(duration=duration).warning(
                "Discovery round took longer than the configured interval. Please investigate."
            )
            INTERVAL_BREACHED_COUNTER.inc()

        time_left = max(interval - duration, 0)
        time.sleep(time_left)


if __name__ == "__main__":
    main()

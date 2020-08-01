import time
from timeit import default_timer

import boto3
from botocore.config import Config
from loguru import logger
from prometheus_client import start_http_server

from prometheus_ecs_discoverer import conf, discovery, fetching, marshalling
from prometheus_ecs_discoverer import settings as s
from prometheus_ecs_discoverer import telemetry

# Copyright 2020 Tim Schwenke. Licensed under the Apache License 2.0


def get_interval_histogram(interval: int):
    steps = 10
    step_size = round(interval / steps, 0)
    return telemetry.histogram(
        "run_duration_seconds",
        "Histogram for duration",
        buckets=[x * step_size for x in range(steps)]
        + [interval + 10, interval + 20, float("inf"),],
    )


def main(
    interval: int = s.INTERVAL,
    directory: str = s.OUTPUT_DIRECTORY,
    should_start_prom_server: bool = s.PROMETHEUS_START_HTTP_SERVER,
    prom_server_port: int = s.PROMETHEUS_SERVER_PORT,
    boto_max_retries: int = s.MAX_RETRY_ATTEMPTS,
    should_warmup_throttle: bool = s.WARMUP_THROTTLE,
    throttle_interval: int = s.THROTTLE_INTERVAL_SECONDS,
) -> None:
    conf.configure_logging()

    DURATION = get_interval_histogram(interval)

    if should_start_prom_server:
        start_http_server(port=prom_server_port)

    # Application logic

    session = boto3.Session()
    config = Config(retries={"max_attempts": s.MAX_RETRY_ATTEMPTS, "mode": "standard"})

    fetcher = fetching.CachedFetcher(
        session.client("ecs", config=config),
        session.client("ec2", config=config),
        should_throttle=should_warmup_throttle,
        throttle_interval_seconds=throttle_interval,
    )

    discoverer = discovery.PrometheusEcsDiscoverer(fetcher)

    first_round = True
    while True:
        start_time = default_timer()

        if not first_round:
            discoverer.fetcher.should_throttle = False

        targets = discoverer.discover()
        marshalling.write_targets_to_file(targets, directory)

        if first_round and should_warmup_throttle:
            fetcher.should_throttle = False
            first_round = False

        duration = max(default_timer() - start_time, 0)

        logger.bind(duration=duration).info("Finished discovery round.")
        DURATION.observe(duration)

        time_left = max(interval - duration, 0)
        time.sleep(time_left)


if __name__ == "__main__":
    main()

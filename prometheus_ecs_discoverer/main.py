import time
from timeit import default_timer

import boto3
from botocore.config import Config
from loguru import logger

from prometheus_ecs_discoverer import conf, discovery, fetching, marshalling
from prometheus_ecs_discoverer import settings as s
from prometheus_ecs_discoverer import telemetry


def main(interval: int = s.INTERVAL, should_warmup_throttle: bool = s.WARMUP_THROTTLE):
    conf.configure_logging()
    steps = 10
    step_size = round(interval / steps, 0)
    DURATION = telemetry.histogram(
        "run_duration_seconds",
        "Histogram for duration",
        buckets=[x * step_size for x in range(steps)]
        + [interval + 10, interval + 20, float("inf"),],
    )

    # Application logic

    session = boto3.Session()
    config = Config(retries={"max_attempts": s.MAX_RETRY_ATTEMPTS, "mode": "standard"})
    ecs_client = session.client("ecs", config=config)
    ec2_client = session.client("ec2", config=config)

    fetcher = fetching.CachedFetcher(ecs_client, ec2_client)

    if should_warmup_throttle:
        fetcher.should_throttle = True
        fetcher.throttle_interval_seconds = s.THROTTLE_INTERVAL_SECONDS

    discoverer = discovery.PrometheusEcsDiscoverer(fetcher)

    first_round = True
    while True:
        start_time = default_timer()

        if not first_round:
            discoverer.fetcher.should_throttle = False

        targets = discoverer.discover()
        marshalling.write_targets_to_file(targets)

        if first_round and should_warmup_throttle:
            fetcher.should_throttle = False
            first_round = False

        duration = max(default_timer() - start_time, 0)

        logger.bind(duration=duration).info("Finished discovery round.")
        DURATION.observe(duration)

        time_left = max(interval - duration, 0)
        time.sleep(time_left)


main()

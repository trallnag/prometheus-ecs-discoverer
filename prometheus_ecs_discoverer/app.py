from prometheus_ecs_discoverer import settings
from prometheus_ecs_discoverer.discovery import PrometheusEcsDiscoverer
from loguru import logger


def main():
    from timeit import default_timer

    x = PrometheusEcsDiscoverer()

    time = default_timer()
    x.discover()
    print(default_timer() - time)


if __name__ == "__main__":
    settings.configure_logging()
    main()

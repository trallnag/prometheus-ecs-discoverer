from prometheus_ecs_discoverer.discovery import PrometheusEcsDiscoverer


def main():
    from timeit import default_timer

    x = PrometheusEcsDiscoverer()

    time = default_timer()
    targets = x.discover()

    print(f"Num of targets: {len(targets)}")
    print(default_timer() - time)


if __name__ == "__main__":
    settings.configure_logging()
    main()

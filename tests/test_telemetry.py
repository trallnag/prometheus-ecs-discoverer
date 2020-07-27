from prometheus_ecs_discoverer import settings as s
from prometheus_ecs_discoverer import telemetry


def test_gauge():
    gauge = telemetry.gauge("gauge", "doc")
    assert gauge._name.startswith(f"{s.PROMETHEUS_NAMESPACE}_{s.PROMETHEUS_SUBSYSTEM}")


def test_counter():
    counter = telemetry.counter("counter", "doc")
    assert counter._name.startswith(f"{s.PROMETHEUS_NAMESPACE}_{s.PROMETHEUS_SUBSYSTEM}")


def test_histogram():
    histogram = telemetry.histogram("gauge", "doc")
    assert histogram._name.startswith(
        f"{s.PROMETHEUS_NAMESPACE}_{s.PROMETHEUS_SUBSYSTEM}"
    )

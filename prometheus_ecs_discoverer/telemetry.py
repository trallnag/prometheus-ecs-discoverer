"""
Helpful wrappers around Prometheus client library. Should be used exclusively
in this package to ensure consistent namespace / subsystem.
"""

from typing import Dict

from prometheus_client import Counter, Gauge, Histogram

from prometheus_ecs_discoverer import s


def gauge(name: str, documentation: str, labels: tuple = ()) -> Gauge:
    """Build a gauge with configured namespace / subsystem."""

    return Gauge(
        name,
        documentation,
        labelnames=labels,
        namespace=s.PROMETHEUS_NAMESPACE,
        subsystem=s.PROMETHEUS_SUBSYSTEM,
    )


def counter(name: str, documentation: str, labels: tuple = ()) -> Counter:
    """Build a counter with configured namespace / subsystem."""

    return Counter(
        name,
        documentation,
        labelnames=labels,
        namespace=s.PROMETHEUS_NAMESPACE,
        subsystem=s.PROMETHEUS_SUBSYSTEM,
    )


def histogram(
    name: str,
    documentation: str,
    labels: tuple = (),
    buckets: tuple = Histogram.DEFAULT_BUCKETS,
) -> Histogram:
    """Build a histogram with configured namespace / subsystem."""

    return Histogram(
        name,
        documentation,
        labelnames=labels,
        namespace=s.PROMETHEUS_NAMESPACE,
        subsystem=s.PROMETHEUS_SUBSYSTEM,
        buckets=buckets,
    )


def info(labels: Dict[str, str], name: str = "info") -> None:
    """Create a gauge with the given label value pairs.

    Helps with exposing static info gauges.
    """

    info_gauge = Gauge(
        name,
        "Info.",
        labelnames=tuple(labels.keys()),
        namespace=s.PROMETHEUS_NAMESPACE,
        subsystem=s.PROMETHEUS_SUBSYSTEM,
    )

    info_gauge.labels(*labels.values()).set(1)

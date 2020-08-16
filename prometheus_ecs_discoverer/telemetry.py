from typing import Dict, Type

from prometheus_client import Counter, Gauge, Histogram

from prometheus_ecs_discoverer import s

# Copyright 2020 Tim Schwenke. Licensed under the Apache License 2.0

"""
Helpful wrappers around Prometheus client library. Should be used exclusively 
in this package to ensure consistent namespace / subsystem.
"""


def gauge(name: str, documentation: str, labels: tuple = ()) -> Type[Gauge]:
    """Builds a gauge with configured namespace / subsystem."""

    return Gauge(
        name,
        documentation,
        labelnames=labels,
        namespace=s.PROMETHEUS_NAMESPACE,
        subsystem=s.PROMETHEUS_SUBSYSTEM,
    )


def counter(name: str, documentation: str, labels: tuple = ()) -> Type[Counter]:
    """Builds a counter with configured namespace / subsystem."""

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
) -> Type[Histogram]:
    """Builds a histogram with configured namespace / subsystem."""

    return Histogram(
        name,
        documentation,
        labelnames=labels,
        namespace=s.PROMETHEUS_NAMESPACE,
        subsystem=s.PROMETHEUS_SUBSYSTEM,
        buckets=buckets,
    )


def info(labels: Dict[str, str], name: str = "info") -> None:
    """Creates a gauge with the given label value pairs.

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

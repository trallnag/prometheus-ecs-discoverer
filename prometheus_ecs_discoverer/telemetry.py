from typing import Dict, Type

from prometheus_client import Counter, Gauge, Histogram

from prometheus_ecs_discoverer import s

# Copyright 2020 Tim Schwenke. Licensed under the Apache License 2.0


def gauge(name: str, documentation: str, labels: tuple = ()) -> Type[Gauge]:
    return Gauge(
        name,
        documentation,
        labelnames=labels,
        namespace=s.PROMETHEUS_NAMESPACE,
        subsystem=s.PROMETHEUS_SUBSYSTEM,
    )


def counter(name: str, documentation: str, labels: tuple = ()) -> Type[Counter]:
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

    Use this function only once during run-time or else Prometheus client 
    library will raise an exception.
    """

    info_gauge = Gauge(
        name,
        "Info.",
        labelnames=tuple(labels.keys()),
        namespace=s.PROMETHEUS_NAMESPACE,
        subsystem=s.PROMETHEUS_SUBSYSTEM,
    )

    info_gauge.labels(*labels.values()).set(1)

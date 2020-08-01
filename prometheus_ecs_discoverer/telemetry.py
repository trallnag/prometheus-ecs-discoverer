from typing import Type

from prometheus_client import Counter, Gauge, Histogram

from prometheus_ecs_discoverer import settings as s

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

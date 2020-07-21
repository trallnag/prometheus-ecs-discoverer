from typing import Type
from prometheus_client import Counter, Gauge, Histogram

from prometheus_ecs_discoverer import settings


def gauge(name: str, documentation: str, labels: tuple = ()) -> Type[Gauge]:
    return Gauge(
        name,
        documentation,
        labelnames=labels,
        namespace=settings.PROMETHEUS_NAMESPACE,
        subsystem=settings.PROMETHEUS_SUBSYSTEM,
    )


def counter(name: str, documentation: str, labels: tuple = ()) -> Type[Counter]:
    return Counter(
        name,
        documentation,
        labelnames=labels,
        namespace=settings.PROMETHEUS_NAMESPACE,
        subsystem=settings.PROMETHEUS_SUBSYSTEM,
    )


def histogram(name: str, documentation: str, labels: tuple = ()) -> Type[Histogram]:
    return Histogram(
        name,
        documentation,
        labelnames=labels,
        namespace=settings.PROMETHEUS_NAMESPACE,
        subsystem=settings.PROMETHEUS_SUBSYSTEM,
    )

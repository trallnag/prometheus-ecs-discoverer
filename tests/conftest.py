import pytest

from prometheus_ecs_discoverer import s


@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    import sys

    from loguru import logger

    logger.remove()

    fmt = "<level>{level}</level> <cyan>{function}</cyan> {message} <dim>{extra}</dim>"
    logger.add(sys.stderr, colorize=True, format=fmt, level="DEBUG")

    s["PRINT_STRUCTS"] = False

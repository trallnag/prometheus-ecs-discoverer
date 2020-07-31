import pytest

from prometheus_ecs_discoverer import settings


@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    import sys

    from loguru import logger

    logger.remove()

    fmt = "<level>{level}</level> <cyan>{function}</cyan> {message} <dim>{extra}</dim>"
    logger.add(sys.stderr, colorize=True, format=fmt, level="DEBUG")

    settings["PRINT_STRUCTS"] = False

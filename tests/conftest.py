import pytest

from prometheus_ecs_discoverer import settings


@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    from loguru import logger
    import sys

    logger.remove()

    fmt = "<level>{level}</level> <cyan>{function}</cyan> {message} <dim>{extra}</dim>"
    logger.add(sys.stderr, colorize=True, format=fmt, level="DEBUG")

    settings["PRINT_STRUCTS"] = False

import os

from dynaconf import Dynaconf
from loguru import logger


current_directory = os.path.dirname(os.path.realpath(__file__))

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[f"{current_directory}/settings/settings.toml",],
)


settings["DEBUG"] = True if settings.LOG_LEVEL == "DEBUG" else False


if settings.boto3_debug:
    import boto3

    boto3.set_stream_logger(name="botocore")


def configure_logging():
    import sys

    logger.remove()

    if settings.log_json:
        fmt = "{message}"
        logger.add(sys.stderr, format=fmt, serialize=True, level=settings.log_level)
    else:
        # <green>{time:HH:mm:ss}</green> <level>{level}</level> <cyan>{name}:{function}:{line}</cyan> {message} <dim>{extra}</dim>
        fmt = "<green>{time:HH:mm:ss}</green> <level>{level}</level> <cyan>{function}</cyan> {message} <dim>{extra}</dim>"
        logger.add(sys.stderr, colorize=True, format=fmt, level=settings.log_level)

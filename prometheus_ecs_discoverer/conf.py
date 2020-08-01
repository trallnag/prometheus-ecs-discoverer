import os

from dynaconf import Dynaconf
from loguru import logger

# Copyright 2020 Tim Schwenke. Licensed under the Apache License 2.0


current_directory = os.path.dirname(os.path.realpath(__file__))

settings = Dynaconf(
    envvar_prefix="DYNACONF", settings_files=[f"{current_directory}/settings.toml",],
)

settings["DEBUG"] = True if settings.LOG_LEVEL == "DEBUG" else False


if settings.boto3_debug:
    import boto3

    boto3.set_stream_logger(name="botocore")


def configure_logging():
    import sys

    logger.remove()

    if settings.LOG_JSON:
        fmt = "{message}"
        logger.add(sys.stderr, format=fmt, serialize=True, level=settings.LOG_LEVEL)
    else:
        # <green>{time:HH:mm:ss}</green> <level>{level}</level> <cyan>{name}:{function}:{line}</cyan> {message} <dim>{extra}</dim>
        fmt = "<green>{time:HH:mm:ss}</green> <level>{level}</level> <cyan>{function}</cyan> {message} <dim>{extra}</dim>"
        logger.add(sys.stderr, colorize=True, format=fmt, level=settings.LOG_LEVEL)

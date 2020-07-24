from loguru import logger


# ==============================================================================
# Configuration constants.

BOTO3_DEBUG_LOGGING = False

# Prometheus -------------------------------------------------------------------

PROMETHEUS_NAMESPACE = "PrometheusEcsDiscoverer_"
PROMETHEUS_SUBSYSTEM = ""

# Logging ----------------------------------------------------------------------

DEBUG = "DEBUG"
INFO = "INFO"
LOGGING_LEVEL = INFO
JSON_LOGGING = False
PRINT_STRUCTURES = False

# ==============================================================================
# Configuration based on constants.

if BOTO3_DEBUG_LOGGING:
    import boto3

    boto3.set_stream_logger(name="botocore")


def configure_logging():
    import sys

    logger.remove()

    if JSON_LOGGING:
        fmt = "{message}"
        logger.add(sys.stderr, format=fmt, serialize=True, level=LOGGING_LEVEL)
    else:
        fmt = "<green>{time:HH:mm:ss}</green> <level>{level}</level> <cyan>{name}:{function}:{line}</cyan> {message} <dim>{extra}</dim>"
        logger.add(sys.stderr, colorize=True, format=fmt, level=LOGGING_LEVEL)

import os

from prometheus_ecs_discoverer import settings


def test_config():
    assert settings.BOTO3_DEBUG is False

    os.environ["DYNACONF_BOTO3_DEBUG"] = "true"
    assert settings.BOTO3_DEBUG is False

    settings["boto3_debug"] = True
    assert settings.BOTO3_DEBUG is True

import os

from prometheus_ecs_discoverer import main, s


def test_config():
    assert s.BOTO3_DEBUG is False

    os.environ["DYNACONF_BOTO3_DEBUG"] = "true"
    assert s.BOTO3_DEBUG is False

    s["boto3_debug"] = True
    assert s.BOTO3_DEBUG is True


def test_expose_info():
    main.expose_info()
    assert True

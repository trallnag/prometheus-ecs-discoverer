import pytest
from loguru import logger

from prometheus_ecs_discoverer import discovery, s

# ==============================================================================
# Tests


def test_extract_custom_labels():
    environment = []
    assert discovery._extract_custom_labels(environment) == {}

    environment = [
        {"name": "WHATEVER", "value": "WHATEVER"},
        {"name": f"{s.CUSTOM_LABEL_PREFIX}another", "value": "WHATEVER"},
        {"name": f"{s.CUSTOM_LABEL_PREFIX}TEST_LABEL", "value": "WHATEVER"},
        {"name": "WHATEVER", "value": "WHATEVER"},
    ]

    labels = discovery._extract_custom_labels(environment)

    assert len(labels) == 2

    assert "another" in labels.keys()
    assert labels["another"] == "WHATEVER"

    assert "test_label" in labels.keys()
    assert labels["test_label"] == "WHATEVER"


# ------------------------------------------------------------------------------


def test_has_proper_network_binding():
    assert (
        discovery._has_proper_network(
            network_bindings=["A", "B"],
            network_interfaces=[],
            network_mode="bridge",
            prom_port=None,
            port_mappings=[],
            scoped_logger=logger,
        )
        is True
    )

    assert (
        discovery._has_proper_network(
            network_bindings=[],
            network_interfaces=[],
            network_mode="awsvpc",
            prom_port=80,
            port_mappings=[],
            scoped_logger=logger,
        )
        is False
    )

    assert (
        discovery._has_proper_network(
            network_bindings=[],
            network_interfaces=[],
            network_mode="host",
            prom_port=80,
            port_mappings=[],
            scoped_logger=logger,
        )
        is True
    )

    assert (
        discovery._has_proper_network(
            network_bindings=[],
            network_interfaces=[],
            network_mode="host",
            prom_port=None,
            port_mappings=["something true"],
            scoped_logger=logger,
        )
        is True
    )


# ------------------------------------------------------------------------------


def test_extract_ip():
    assert (
        discovery._extract_ip(
            network_mode="host",
            network_interfaces=["does not matter"],
            ec2_instance={"PrivateIpAddress": "important"},
        )
        == "important"
    )

    assert (
        discovery._extract_ip(
            network_mode="awsvpc",
            network_interfaces=[
                {"privateIpv4Address": "important"},
                {"privateIpv4Address": "not important"},
            ],
            ec2_instance={"PrivateIpAddress": "not important"},
        )
        == "important"
    )

    with pytest.raises(Exception):
        discovery._extract_ip(
            network_mode="awsvpc",
            network_interfaces=[],
            ec2_instance={"PrivateIpAddress": "not important"},
        )


# ------------------------------------------------------------------------------


def test_extract_port():
    assert (
        discovery._extract_port(
            network_mode=None,
            prom_port="145",
            prom_container_port=None,
            port_mappings=[],
            network_bindings=[],
        )
        == "145"
    )

    assert (
        discovery._extract_port(
            network_mode="host",
            prom_port=None,
            prom_container_port=None,
            port_mappings=[{"hostPort": "123"}],
            network_bindings=[],
        )
        == "123"
    )

    assert (
        discovery._extract_port(
            network_mode="awsvpc",
            prom_port=None,
            prom_container_port=None,
            port_mappings=[],
            network_bindings=[],
        )
        == "80"
    )

    assert (
        discovery._extract_port(
            network_mode="bridge",
            prom_port=None,
            prom_container_port="123",
            port_mappings=[],
            network_bindings=[{"containerPort": 123, "hostPort": 100}],
        )
        == "100"
    )

    assert (
        discovery._extract_port(
            network_mode="bridge",
            prom_port=None,
            prom_container_port="123",
            port_mappings=[],
            network_bindings=[
                {"containerPort": 124, "hostPort": 101},
                {"containerPort": 123, "hostPort": 100},
            ],
        )
        == "100"
    )

    assert (
        discovery._extract_port(
            network_mode="bridge",
            prom_port=None,
            prom_container_port="123",
            port_mappings=[],
            network_bindings=[{"containerPort": 124, "hostPort": 100}],
        )
        is None
    )

    assert (
        discovery._extract_port(
            network_mode="bridge",
            prom_port=None,
            prom_container_port=None,
            port_mappings=[],
            network_bindings=[{"containerPort": 124, "hostPort": 100}],
        )
        == "100"
    )

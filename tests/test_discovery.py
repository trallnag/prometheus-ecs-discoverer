import warnings

warnings.filterwarnings(action="ignore", category=DeprecationWarning, module=r"boto")
warnings.filterwarnings(action="ignore", category=DeprecationWarning, module=r"moto")

import os
import json
from typing import Type

import boto3
from moto import mock_ecs, mock_ec2
from moto.ec2 import utils as ec2_utils
import pytest

from prometheus_ecs_discoverer.discovery import PrometheusEcsDiscoverer
from prometheus_ecs_discoverer.toolbox import print_structure
from prometheus_ecs_discoverer import settings


settings.configure_logging()


# ==============================================================================
# Fixtures

# We use moto library to create a mocked AWS environment.


@pytest.fixture(scope="function")
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture(scope="function")
def ecs_client(aws_credentials):
    with mock_ecs():
        yield boto3.client("ecs", region_name="us-east-1")


@pytest.fixture(scope="function")
def ec2_client(aws_credentials):
    with mock_ec2():
        yield boto3.client("ec2", region_name="us-east-1")


@pytest.fixture(scope="function")
def ec2_resource(aws_credentials):
    with mock_ec2():
        yield boto3.resource("ec2", region_name="us-east-1")


@pytest.fixture(scope="function")
def discoverer(ecs_client, ec2_client) -> Type[PrometheusEcsDiscoverer]:
    yield PrometheusEcsDiscoverer(ecs_client=ecs_client, ec2_client=ec2_client)


@pytest.fixture(scope="function")
def expected(ecs_client, ec2_client, ec2_resource) -> dict:
    instance_count = 3

    info_dict = {}

    # cluster ------------------------------------------------------------------

    cluster_response = ecs_client.create_cluster(
        capacityProviders=["EC2"], clusterName="cluster"
    )
    cluster_arn = cluster_response["cluster"]["clusterArn"]
    print(f"cluster_arn={cluster_arn}")
    info_dict["cluster_arn"] = cluster_arn

    # instances ----------------------------------------------------------------

    instances = ec2_resource.create_instances(
        ImageId="ami-bb9a6bc2",
        MinCount=instance_count,
        MaxCount=instance_count,
        InstanceType="t3a.medium",
    )
    instance_ids = [instance.id for instance in instances]
    info_dict["instance_ids"] = instance_ids
    print_structure(instance_ids, "instance_ids")

    # _instances = ec2_client.describe_instances()["Reservations"][0]["Instances"]
    # print_structure(_instances, "instances")

    # register instances as ecs ------------------------------------------------

    for instance in instances:
        ecs_client.register_container_instance(
            cluster=cluster_arn,
            instanceIdentityDocument=json.dumps(
                ec2_utils.generate_instance_identity_document(instance)
            ),
        )

    container_instances = ecs_client.list_container_instances(cluster=cluster_arn)
    # print_structure(
    #     container_instances, f"list_container_instances(cluster={cluster_arn})",
    # )

    container_instance_ids = [
        arn.split("/")[-1] for arn in container_instances["containerInstanceArns"]
    ]
    info_dict["container_instance_arns"] = container_instances["containerInstanceArns"]
    print_structure(container_instance_ids, "container_instance_ids")

    # register task definitions ------------------------------------------------

    ecs_client.register_task_definition(
        family="task_irrelevant_1",
        containerDefinitions=[
            {
                "name": "container_irrelevant_1",
                "image": "docker/hello-world:latest",
                "cpu": 10,
                "memory": 10,
                "environment": [
                    {"name": "AWS_ACCESS_KEY_ID", "value": "SOME_ACCESS_KEY"}
                ],
                "logConfiguration": {"logDriver": "json-file"},
            }
        ],
    )

    ecs_client.register_task_definition(
        family="task_relevant_1",
        containerDefinitions=[
            {
                "name": "container_relevant_1",
                "image": "docker/hello-world:latest",
                "environment": [
                    {"name": "PROMETHEUS", "value": "does not matter"},
                    {"name": "PROMETHEUS_CUSTOM_type", "value": "XXXXX"},
                    {"name": "PROMETHEUS_CUSTOM_whatever", "value": "XXXXXeffgef de"},
                    {"name": "PROMETHEUS_ENDPOINT", "value": "/metrics"},
                ],
                "logConfiguration": {"logDriver": "json-file"},
                "portMappings": [{"containerPort": 80, "hostPort": 0, "protocol": "tcp"}],
                "memory": 10,
            }
        ],
    )

    info_dict["task_definition_arns"] = ecs_client.list_task_definitions().get(
        "taskDefinitionArns"
    )
    print_structure(ecs_client.list_task_definitions(), "list_task_definitions")

    # start tasks --------------------------------------------------------------

    ecs_client.run_task(
        cluster=cluster_arn,
        count=2,
        launchType="EC2",
        taskDefinition="task_irrelevant_1",
        startedBy="foo",
    )

    ecs_client.run_task(
        cluster=cluster_arn,
        count=3,
        launchType="EC2",
        taskDefinition="task_relevant_1",
        startedBy="foo",
    )

    # --------------------------------------------------------------------------

    yield info_dict


# ==============================================================================
# Tests


def test_overall(expected, discoverer: Type[PrometheusEcsDiscoverer]):
    targets = discoverer.discover()
    assert len(targets) == 3


# ==============================================================================
# Misc tests.


def test_extract_cluster_name():
    cluster_arn = "arn:aws:ecs:eu-central-1:4342432423:cluster/data-cluster"
    cluster_name = cluster_arn.split("/")[-1]
    assert cluster_name == "data-cluster"

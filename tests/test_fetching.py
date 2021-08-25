import warnings

warnings.filterwarnings(action="ignore", category=DeprecationWarning, module=r"boto")
warnings.filterwarnings(action="ignore", category=DeprecationWarning, module=r"moto")

import json
import os
from dataclasses import dataclass
from timeit import default_timer
from typing import Any, Generator, Type

import boto3
import pytest
from moto import mock_ec2, mock_ecs
from moto.ec2 import utils as ec2_utils

from prometheus_ecs_discoverer import toolbox
from prometheus_ecs_discoverer.fetching import CachedFetcher

# ==============================================================================
# Fixtures


@dataclass
class Boto:
    client: Any
    resource: Any


@pytest.fixture(scope="function")
def aws_credentials() -> None:
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture(scope="function")
def ecs(aws_credentials) -> Generator:
    with mock_ecs():
        yield Boto(client=boto3.client("ecs", region_name="us-east-1"), resource=None)


@pytest.fixture(scope="function")
def ec2(aws_credentials) -> Generator:
    with mock_ec2():
        yield Boto(
            client=boto3.client("ec2", region_name="us-east-1"),
            resource=boto3.resource("ec2", region_name="us-east-1"),
        )


@pytest.fixture(scope="function")
def fetcher(ecs: Type[Boto], ec2: Boto) -> CachedFetcher:
    return CachedFetcher(ecs.client, ec2.client)


# ==============================================================================
# Tests


def test_throttle(fetcher, ecs):
    start_time = default_timer()
    _ = fetcher.get_cluster_arns()
    duration = max(default_timer() - start_time, 0)
    assert duration < 1

    fetcher.should_throttle = True
    fetcher.throttle_interval_seconds = 1

    start_time = default_timer()
    _ = fetcher.get_cluster_arns()
    duration = max(default_timer() - start_time, 0)
    assert duration > 1


def test_get_cluster_arns(fetcher, ecs):
    response = ecs.client.create_cluster(clusterName="test_ecs_cluster")

    cluster_arns = fetcher.get_cluster_arns()

    assert len(cluster_arns) == 1
    assert cluster_arns[0] == response["cluster"]["clusterArn"]


# ------------------------------------------------------------------------------


def test_get_container_instance_arns(fetcher, ecs, ec2):
    cluster_name = "test_ecs_cluster"

    response = ecs.client.create_cluster(clusterName=cluster_name)
    cluster_arn = response["cluster"]["clusterArn"]

    test_instance = ec2.resource.create_instances(
        ImageId="ami-bb9a6bc2", MinCount=1, MaxCount=1
    )[0]

    instance_id_document = json.dumps(
        ec2_utils.generate_instance_identity_document(test_instance)
    )

    response = ecs.client.register_container_instance(
        cluster=cluster_name, instanceIdentityDocument=instance_id_document
    )
    expected_container_instance_arn = response["containerInstance"][
        "containerInstanceArn"
    ]

    assert response["containerInstance"]["ec2InstanceId"] == test_instance.id

    container_instance_arns = fetcher.get_container_instance_arns(cluster_arn=cluster_arn)

    assert len(container_instance_arns) == 1
    assert container_instance_arns[0] == expected_container_instance_arn


# ------------------------------------------------------------------------------


def test_get_task_definition_arns(fetcher, ecs, ec2):
    cluster_name = "test_ecs_cluster"

    _ = ecs.client.create_cluster(clusterName=cluster_name)

    test_instances = ec2.resource.create_instances(
        ImageId="ami-bb9a6bc2", MinCount=3, MaxCount=3
    )

    for test_instance in test_instances:
        instance_id_document = json.dumps(
            ec2_utils.generate_instance_identity_document(test_instance)
        )
        _ = ecs.client.register_container_instance(
            cluster=cluster_name, instanceIdentityDocument=instance_id_document
        )

    response = ecs.client.register_task_definition(
        family="test_ecs_task",
        containerDefinitions=[
            {
                "name": "hello_world",
                "image": "docker/hello-world:latest",
                "cpu": 1024,
                "memory": 400,
                "essential": True,
                "logConfiguration": {"logDriver": "json-file"},
            }
        ],
    )
    toolbox.pstruct(response["taskDefinition"], "register_task_definition")

    task_definition_arns = fetcher.get_task_definition_arns()

    assert len(task_definition_arns) == 1
    assert task_definition_arns[0] == response["taskDefinition"]["taskDefinitionArn"]


# ------------------------------------------------------------------------------


def test_get_task_arns_with_run_task(fetcher, ecs, ec2):
    cluster_name = "test_ecs_cluster"

    response = ecs.client.create_cluster(clusterName=cluster_name)
    cluster_arn = response["cluster"]["clusterArn"]

    test_instances = ec2.resource.create_instances(
        ImageId="ami-bb9a6bc2", MinCount=3, MaxCount=3
    )

    for test_instance in test_instances:
        instance_id_document = json.dumps(
            ec2_utils.generate_instance_identity_document(test_instance)
        )
        _ = ecs.client.register_container_instance(
            cluster=cluster_name, instanceIdentityDocument=instance_id_document
        )

    _ = ecs.client.register_task_definition(
        family="test_ecs_task",
        containerDefinitions=[
            {
                "name": "hello_world",
                "image": "docker/hello-world:latest",
                "cpu": 1024,
                "memory": 400,
                "essential": True,
                "logConfiguration": {"logDriver": "json-file"},
            }
        ],
    )

    response_ec2 = ecs.client.run_task(
        cluster=cluster_name,
        overrides={},
        taskDefinition="test_ecs_task",
        count=2,
        launchType="EC2",
        startedBy="moto",
    )
    toolbox.pstruct(response, "run_task ec2")

    _ = ecs.client.run_task(
        cluster=cluster_name,
        overrides={},
        taskDefinition="test_ecs_task",
        count=1,
        launchType="EC2",
        startedBy="moto",
    )
    toolbox.pstruct(response, "run_task fargate")

    assert len(response_ec2["tasks"]) == 2

    # Currently moto does not support launch type.
    assert "EC2" != response_ec2["tasks"][0].get("launchType", None)
    assert "EC2" != response_ec2["tasks"][1].get("launchType", None)

    task_arns = fetcher.get_task_arns(cluster_arn=cluster_arn)
    assert len(task_arns) == 3


# ------------------------------------------------------------------------------


def test_get_tasks(fetcher, ecs, ec2):
    cluster_name = "test_ecs_cluster"

    response = ecs.client.create_cluster(clusterName=cluster_name)
    cluster_arn = response["cluster"]["clusterArn"]

    test_instances = ec2.resource.create_instances(
        ImageId="ami-bb9a6bc2", MinCount=3, MaxCount=3
    )

    for test_instance in test_instances:
        instance_id_document = json.dumps(
            ec2_utils.generate_instance_identity_document(test_instance)
        )
        _ = ecs.client.register_container_instance(
            cluster=cluster_name, instanceIdentityDocument=instance_id_document
        )

    _ = ecs.client.register_task_definition(
        family="test_ecs_task",
        containerDefinitions=[
            {
                "name": "hello_world",
                "image": "docker/hello-world:latest",
                "cpu": 1024,
                "memory": 400,
                "essential": True,
                "logConfiguration": {"logDriver": "json-file"},
            }
        ],
    )

    response = ecs.client.run_task(
        cluster=cluster_name,
        overrides={},
        taskDefinition="test_ecs_task",
        count=2,
        launchType="EC2",
        startedBy="moto",
    )

    tasks = fetcher.get_tasks(cluster_arn=cluster_arn)

    assert len(tasks) == 2
    assert response["tasks"][0]["taskArn"] in tasks.keys()
    assert response["tasks"][1]["taskArn"] in tasks.keys()

    tasks = fetcher.get_tasks(
        cluster_arn=cluster_arn, task_arns=fetcher.get_task_arns(cluster_arn=cluster_arn)
    )

    assert len(tasks) == 2
    assert response["tasks"][0]["taskArn"] in tasks.keys()
    assert response["tasks"][1]["taskArn"] in tasks.keys()


# ------------------------------------------------------------------------------


def test_get_container_instances(fetcher, ecs, ec2):
    cluster_name = "test_ecs_cluster"

    response = ecs.client.create_cluster(clusterName=cluster_name)
    cluster_arn = response["cluster"]["clusterArn"]

    test_instances = ec2.resource.create_instances(
        ImageId="ami-bb9a6bc2", MinCount=3, MaxCount=3
    )

    instance_id_document = json.dumps(
        ec2_utils.generate_instance_identity_document(test_instances[0])
    )
    response = ecs.client.register_container_instance(
        cluster=cluster_name, instanceIdentityDocument=instance_id_document
    )
    toolbox.pstruct(response, "register_container_instance")

    container_instances = fetcher.get_container_instances(cluster_arn)

    assert len(container_instances) == 1
    assert (
        response["containerInstance"]["containerInstanceArn"]
        in container_instances.keys()
    )

    container_instances = fetcher.get_container_instances(
        cluster_arn, arns=fetcher.get_container_instance_arns(cluster_arn)
    )

    assert len(container_instances) == 1
    assert (
        response["containerInstance"]["containerInstanceArn"]
        in container_instances.keys()
    )


# ------------------------------------------------------------------------------


def test_get_ec2_instances(fetcher, ecs, ec2):
    test_instances = ec2.resource.create_instances(
        ImageId="ami-bb9a6bc2", MinCount=3, MaxCount=3
    )
    toolbox.pstruct(test_instances, "c2.resource.create_instances")

    ids = [instance.id for instance in test_instances]

    ec2_instances = fetcher.get_ec2_instances(ids)

    assert len(ec2_instances) == 3

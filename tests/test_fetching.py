import warnings

warnings.filterwarnings(action="ignore", category=DeprecationWarning, module=r"boto")
warnings.filterwarnings(action="ignore", category=DeprecationWarning, module=r"moto")

import os
from pprint import pprint
from typing import Type
import json

import boto3
from moto import mock_ecs, mock_ec2
from moto.ec2 import utils as ec2_utils
import pytest

from prometheus_ecs_discoverer.fetching import CachedFetcher


# ==============================================================================
# Fixtures


@pytest.fixture(scope="function")
def aws_credentials() -> object:
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
def fetcher(ecs_client, ec2_client) -> Type[CachedFetcher]:
    yield CachedFetcher(ecs_client, ec2_client)


# ==============================================================================
# Helpers


def print_structure(data, name: str = "generic"):
    print("=" * 70)
    print(name)
    pprint(data)
    print(" ")


def setup_ecs(ecs_client, ec2_resource, instance_count: int = 3) -> dict:
    info_dict = {
        "cluster_arn": None,
    }

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
        InstanceType="t2.micro",
    )
    instance_ids = [instance.id for instance in instances]
    info_dict["instance_ids"] = instance_ids
    print(f"instance_ids={instance_ids}")

    # register instances as ecs ------------------------------------------------

    for instance in instances:
        ecs_client.register_container_instance(
            cluster=cluster_arn,
            instanceIdentityDocument=json.dumps(
                ec2_utils.generate_instance_identity_document(instance)
            ),
        )

    container_instances = ecs_client.list_container_instances(cluster=cluster_arn)
    print_structure(
        container_instances, f"list_container_instances(cluster={cluster_arn})",
    )

    container_instance_ids = [
        arn.split("/")[-1] for arn in container_instances["containerInstanceArns"]
    ]
    info_dict["container_instance_arns"] = container_instances["containerInstanceArns"]
    print_structure(container_instance_ids, "container_instance_ids")

    # register task definitions ------------------------------------------------

    ecs_client.register_task_definition(
        family="task_definition_0",
        containerDefinitions=[
            {
                "name": "hello_world_0",
                "image": "docker/hello-world:latest",
                "cpu": 1024,
                "memory": 400,
                "environment": [
                    {"name": "AWS_ACCESS_KEY_ID", "value": "SOME_ACCESS_KEY"}
                ],
                "logConfiguration": {"logDriver": "json-file"},
            }
        ],
    )

    ecs_client.register_task_definition(
        family="task_definition_1",
        containerDefinitions=[
            {
                "name": "hello_world_1",
                "image": "docker/hello-world:latest",
                "cpu": 1024,
                "memory": 400,
                "environment": [
                    {"name": "AWS_ACCESS_KEY_ID", "value": "SOME_ACCESS_KEY"}
                ],
                "logConfiguration": {"logDriver": "json-file"},
            }
        ],
    )

    info_dict["task_definition_arns"] = ecs_client.list_task_definitions().get(
        "taskDefinitionArns"
    )
    print_structure(ecs_client.list_task_definitions(), "list_task_definitions")

    # start tasks --------------------------------------------------------------

    ecs_client.start_task(
        cluster=cluster_arn,
        taskDefinition="task_definition_0",
        overrides={},
        containerInstances=container_instance_ids,
        startedBy="foo",
    )

    ecs_client.start_task(
        cluster=cluster_arn,
        taskDefinition="task_definition_1",
        overrides={},
        containerInstances=[container_instance_ids[0]],
        startedBy="foo",
    )

    print_structure(ecs_client.list_tasks(), "list_tasks")
    info_dict["task_arns"] = ecs_client.list_tasks()["taskArns"]

    # --------------------------------------------------------------------------

    return info_dict


# ==============================================================================
# get_cluster_arns


def test_get_cluster_arns(ecs_client, ec2_client, fetcher):
    cluster1_arn = (
        ecs_client.create_cluster(capacityProviders=["EC2"], clusterName="cluster1")
        .get("cluster")
        .get("clusterArn")
    )
    cluster2_arn = (
        ecs_client.create_cluster(capacityProviders=["FARGATE"], clusterName="cluster2")
        .get("cluster")
        .get("clusterArn")
    )

    arns = fetcher.get_cluster_arns()
    print_structure(arns, "cluster arns")
    assert len(arns) == 2
    assert cluster1_arn in arns
    assert cluster2_arn in arns


def test_get_cluster_arns_no_clusters(ecs_client, ec2_client, fetcher):
    arns = fetcher.get_cluster_arns()
    print_structure(arns, "cluster arns")
    assert arns == []


def test_get_cluster_arns_with_mock(
    ecs_client, ec2_client, ec2_resource, fetcher: Type[CachedFetcher]
):
    expected = setup_ecs(ecs_client, ec2_resource)
    cluster_arns = fetcher.get_cluster_arns()
    print_structure(cluster_arns, "cluster_arns")
    assert cluster_arns == [expected["cluster_arn"]]


# ==============================================================================
# get_task_arns


def test_get_task_arns(ecs_client, ec2_resource, fetcher: Type[CachedFetcher]):
    expected = setup_ecs(ecs_client, ec2_resource)
    task_arns = fetcher.get_task_arns(expected["cluster_arn"], "EC2")
    print_structure(task_arns, "task_arns")
    assert len(task_arns) == len(expected["task_arns"])
    for expected_arn in expected["task_arns"]:
        assert expected_arn in task_arns


def test_get_task_arns_no_tasks(fetcher: Type[CachedFetcher]):
    task_arns = fetcher.get_task_arns("", "EC2")
    print_structure(task_arns, "task_arns")
    assert task_arns == []


# ==============================================================================
# get_tasks


def test_get_tasks_with_arns(ecs_client, ec2_resource, fetcher: Type[CachedFetcher]):
    expected = setup_ecs(ecs_client, ec2_resource)
    tasks = fetcher.get_tasks(expected["cluster_arn"], expected["task_arns"])
    print_structure(tasks, "tasks")
    for key in tasks:
        assert key in expected["task_arns"]


def test_get_tasks_with_no_arns(ecs_client, ec2_resource, fetcher: Type[CachedFetcher]):
    expected = setup_ecs(ecs_client, ec2_resource)
    tasks = fetcher.get_tasks(expected["cluster_arn"])
    print_structure(tasks, "tasks")
    for key in tasks:
        assert key in expected["task_arns"]


# ==============================================================================
# get_task_definition_arns


def test_get_task_definition_arns(ecs_client, ec2_resource, fetcher: Type[CachedFetcher]):
    expected = setup_ecs(ecs_client, ec2_resource)
    task_definition_arns = fetcher.get_task_definition_arns()
    print_structure(task_definition_arns, "task_definition_arns")
    for arn in task_definition_arns:
        assert arn in expected["task_definition_arns"]


def test_get_task_definition_arns_no_defs(fetcher: Type[CachedFetcher]):
    task_definition_arns = fetcher.get_task_definition_arns()
    assert task_definition_arns == []


# ==============================================================================
# get_task_definitions


def test_get_task_definitions(ecs_client, ec2_resource, fetcher: Type[CachedFetcher]):
    expected = setup_ecs(ecs_client, ec2_resource)
    task_definitions = fetcher.get_task_definitions(expected.get("task_definition_arns"))
    print_structure(task_definitions, "task_definitions")
    for key in task_definitions:
        assert key in expected["task_definition_arns"]


# ==============================================================================
# Container instances.


def test_get_container_instance_arns(
    ecs_client, ec2_resource, fetcher: Type[CachedFetcher]
):
    expected = setup_ecs(ecs_client, ec2_resource)
    container_instance_arns = fetcher.get_container_instance_arns(expected["cluster_arn"])
    print_structure(container_instance_arns, "container_instance_arns")
    for arn in container_instance_arns:
        assert arn in expected["container_instance_arns"]


def test_get_container_instance_arns_no_defs(fetcher: Type[CachedFetcher]):
    container_instance_arns = fetcher.get_container_instance_arns("")
    assert container_instance_arns == []


def test_get_container_instances(ecs_client, ec2_resource, fetcher: Type[CachedFetcher]):
    expected = setup_ecs(ecs_client, ec2_resource)
    container_instances = fetcher.get_container_instances(
        expected["cluster_arn"], expected["container_instance_arns"]
    )
    print_structure(container_instances, "container_instances")
    assert len(container_instances) > 0
    for key in container_instances:
        assert (
            container_instances[key]["containerInstanceArn"]
            in expected["container_instance_arns"]
        )


# ==============================================================================
# get_ec2_instances


def test_get_ec2_instances(ecs_client, ec2_resource, fetcher: Type[CachedFetcher]):
    expected = setup_ecs(ecs_client, ec2_resource)
    ec2_instances = fetcher.get_ec2_instances(expected["instance_ids"])
    print_structure(ec2_instances, "ec2_instances")
    assert len(ec2_instances) > 0
    for key in ec2_instances:
        assert key in expected["instance_ids"]

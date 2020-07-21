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


def mock_aws(ecs_client, ec2_client, ec2_resource):
    cluster_response = ecs_client.create_cluster(
        capacityProviders=["EC2"], clusterName="cluster"
    )
    cluster_arn = cluster_response["cluster"]["clusterArn"]
    print(f"cluster_arn={cluster_arn}")

    instances = ec2_resource.create_instances(
        ImageId="ami-bb9a6bc2", MinCount=2, MaxCount=2, InstanceType="t2.micro"
    )
    instance_ids = [instance.id for instance in instances]
    print(f"instance_ids={instance_ids}")

    for instance in instances:
        ecs_client.register_container_instance(
            cluster=cluster_arn,
            instanceIdentityDocument=json.dumps(
                ec2_utils.generate_instance_identity_document(instance)
            ),
        )
    print_structure(
        ecs_client.list_container_instances(cluster=cluster_arn),
        f"list_container_instances(cluster={cluster_arn})",
    )

    # Register task definitions
    # Create tasks


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


# ==============================================================================
# get_task_arns


def test_get_task_arns(ecs_client, ec2_client, ec2_resource, fetcher):
    mock_aws(ecs_client, ec2_client, ec2_resource)
    assert 1 == 2

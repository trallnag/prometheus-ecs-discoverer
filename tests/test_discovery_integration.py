import os

import botocore
from botocore.stub import Stubber

from prometheus_ecs_discoverer import discovery, toolbox, fetching
from tests import test_discovery_integration_data as data


def test_discovery_full():
    os.environ["AWS_DEFAULT_REGION"] = "eu-central-1"
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"

    ecs_client = botocore.session.get_session().create_client("ecs")
    ec2_client = botocore.session.get_session().create_client("ec2")

    ecs_stubber = Stubber(ecs_client)
    ec2_stubber = Stubber(ec2_client)

    # ----------------------------------------------------------------------
    # Preload stubbers with everything necessary.

    ecs_stubber.add_response("list_clusters", data.list_clusters_response, {})

    ecs_stubber.add_response(
        "list_tasks", data.list_tasks_response, data.list_tasks_parameters
    )

    ecs_stubber.add_response(
        "list_container_instances",
        data.list_container_instances_response,
        data.list_container_instances_parameters,
    )

    ecs_stubber.activate()
    ec2_stubber.activate()

    # --------------------------------------------------------------------------

    discoverer = discovery.PrometheusEcsDiscoverer(
        ecs_client=ecs_client, ec2_client=ec2_client
    )
    fetcher = fetching.CachedFetcher(ecs_client, ec2_client)
    discoverer.fetcher = fetcher

    # Inject data into caches.

    fetcher.task_cache.current = toolbox.list_to_dict(
        data.describe_tasks_response["tasks"], "taskArn"
    )

    fetcher.task_definition_cache.current = {}
    for task_definition in data.describe_task_definition_responses:
        fetcher.task_definition_cache.current[
            task_definition["taskDefinition"]["taskDefinitionArn"]
        ] = task_definition["taskDefinition"]

    fetcher.container_instance_cache.current = toolbox.list_to_dict(
        data.describe_container_instances_response["containerInstances"],
        "containerInstanceArn",
    )

    fetcher.ec2_instance_cache.current = {}
    for reservation in data.describe_instances_response["Reservations"]:
        for instance in reservation["Instances"]:
            fetcher.ec2_instance_cache.current[instance["InstanceId"]] = instance

    targets = discoverer.discover()

    assert len(targets) == 6

    target = targets[0]

    assert target.ip == "10.0.2.85"
    assert target.port == "32794"
    assert target.p_instance == "10.0.2.85:32794"
    assert target.task_name == "webapp-test-3"
    assert target.metrics_path == "/app-3/metrics"
    assert target.cluster_name == "cluster-name"
    assert target.task_version == "2"
    assert target.task_id == "550b823c-288a-4f31-b3e1-69f9ea15060d"
    assert target.container_id == "213d21d5-4718-4b7f-9f7d-a1b3a8e57ad8"
    assert target.instance_id == "i-0b967c2479dd4f5af"
    assert target.custom_labels == {}

    toolbox.pstruct(targets, "targets")

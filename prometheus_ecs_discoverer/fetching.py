from typing import Dict, List
import logging

from prometheus_ecs_discoverer import telemetry
from prometheus_ecs_discoverer import toolbox
from prometheus_ecs_discoverer.caching import SlidingCache


logger = logging.getLogger(__name__)

REQUESTS = telemetry.counter(
    "api_requests", "Number of requests made to the AWS API.", ("method",)
)


class CachedFetcher:
    """Works with the AWS API and leverages a sliding cache.

    Reduces the amount of request made to the AWS API helping to stay below the 
    request limits. Only implements necessary methods. So not a generic class.

    Rember to flush all caches with `flush_caches()` after every "full round".
    """

    def __init__(self, ecs_client, ec2_client):
        self.ecs = ecs_client
        self.ec2 = ec2_client
        self.task_cache = SlidingCache(name="task_cache")
        self.task_definition_cache = SlidingCache(name="task_definition_cache")
        self.container_instance_cache = SlidingCache(name="container_instance_cache")
        self.ec2_instance_cache = SlidingCache(name="ec2_instance_cache")

    def flush_caches(self) -> None:
        self.task_cache.flush()
        self.task_definition_cache.flush()
        self.container_instance_cache.flush()
        self.ec2_instance_cache.flush()

    def get_arns(self, method: str, key: str, **aws_api_parameters) -> List[str]:
        arns = []
        for page in self.ecs.get_paginator(method).paginate(**aws_api_parameters):
            REQUESTS.labels(method).inc()
            arns += page.get(key, [])
        return arns

    def get_cluster_arns(self) -> List[str]:
        return self.get_arns("list_clusters", "clusterArns")

    def get_task_arns(self, cluster_arn: str, launch_type: str = None) -> List[str]:
        if launch_type:
            return self.get_arns(
                "list_tasks", "taskArns", cluster=cluster_arn, launchType=launch_type
            )
        else:
            return self.get_arns("list_tasks", "taskArns", cluster=cluster_arn)

    def get_task_definition_arns(self) -> List[str]:
        return self.get_arns("list_task_definitions", "taskDefinitionArns")

    def get_container_instance_arns(self, cluster_arn: str) -> List[str]:
        return self.get_arns(
            "list_container_instances", "containerInstanceArns", cluster=cluster_arn
        )

    def get_tasks(self, cluster_arn: str, task_arns: List[str] = None) -> Dict[str, dict]:
        """Get task descriptions.

        :param task_arns: Defaults to `None`. This will trigger this method to 
            fetch the task ARNs for the given cluster.
        :return: Dictionary. Every entry represents a task. Keys are the 
            respective ARNs.
        
        [Boto3 API Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.describe_tasks)
        """

        def uncached_fetch(task_arns: List[str]) -> dict:
            tasks = []
            chunked_task_arns = toolbox.chunk_list(task_arns, 100)

            for task_arns_chunk in chunked_task_arns:
                tasks += self.ecs.describe_tasks(
                    cluster=cluster_arn, tasks=task_arns_chunk
                )["tasks"]
                REQUESTS.labels("describe_tasks").inc()

            return toolbox.list_to_dict(tasks, "taskArn")

        if task_arns is None:
            task_arns = self.get_task_arns(cluster_arn)

        return self.task_cache.get_multiple(task_arns, uncached_fetch)

    def get_task_definition(self, task_definition_arn: str) -> dict:
        """Get single task definition.

        [Boto3 API Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.describe_task_definition)
        """

        def uncached_fetch(task_definition_arn: str) -> dict:
            response = self.ecs.describe_task_definition(
                taskDefinition=task_definition_arn
            )
            REQUESTS.labels("describe_task_definition").inc()
            return response["taskDefinition"]

        return self.task_definition_cache.get_single(task_definition_arn, uncached_fetch)

    def get_task_definitions(
        self, task_definition_arns: List[str] = None
    ) -> Dict[str, dict]:
        """Get task definition descriptions.
        
        :param task_definition_arns: ARNs of task definitions to retrieve. 
            Defaults to `None`.
        :return: Dictionary wher every entry represents a task definition 
            description. Keys are the respective ARNs.

        [Boto3 API Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.describe_task_definition)
        """

        def uncached_fetch(task_definition_arns: List[str]) -> Dict[str, dict]:
            descriptions = {}
            for arn in task_definition_arns:
                response = self.ecs.describe_task_definition(taskDefinition=arn)
                REQUESTS.labels("describe_task_definition").inc()
                response_arn = response["taskDefinition"]["taskDefinitionArn"]
                descriptions[response_arn] = response["taskDefinition"]

            return descriptions

        if task_definition_arns is None:
            task_definition_arns = self.get_task_definition_arns()

        return self.task_definition_cache.get_multiple(
            task_definition_arns, uncached_fetch,
        )

    def get_container_instances(
        self, cluster_arn: str, container_instance_arns: List[str] = None
    ) -> Dict[str, dict]:
        """Get container instance descriptions.

        :param cluster_arn: ARN of the instances' cluster.
        :param container_instance_arns: List of container instance ARNs.
        :return: Dictionary wher every entry represents a container instance 
            definition description. Keys are the respective ARNs.

        [Boto3 API Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.describe_container_instances)
        """

        def uncached_fetch(container_instance_arns: List[str]) -> Dict[str, dict]:
            lst = []
            arns_chunks = toolbox.chunk_list(container_instance_arns, 100)

            for arns_chunk in arns_chunks:
                lst += self.ecs.describe_container_instances(
                    cluster=cluster_arn, containerInstances=arns_chunk
                )["containerInstances"]
                REQUESTS.labels("describe_container_instances").inc()

            return toolbox.list_to_dict(lst, "containerInstanceArn")

        if container_instance_arns is None:
            container_instance_arns = self.get_container_instance_arns(cluster_arn)

        return self.container_instance_cache.get_multiple(
            container_instance_arns, uncached_fetch,
        )

    def get_ec2_instances(self, instance_ids: List[str]) -> Dict[str, dict]:
        """Get EC2 instance descriptions.

        :param instance_ids: Instance IDs to describe.
        :return: Dictionary wher every entry represents an EC2 instance 
            description. Keys are the respective instance IDs.

        [Boto3 API Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances)
        """

        def uncached_fetch(instance_ids: List[str]) -> Dict[str, dict]:
            instances_list = []
            ids_chunks = toolbox.chunk_list(instance_ids, 100)

            for ids_chunk in ids_chunks:
                response = self.ec2.describe_instances(InstanceIds=ids_chunk)
                for reservation in response["Reservations"]:
                    instances_list += reservation["Instances"]
                REQUESTS.labels("describe_instances").inc()

            return toolbox.list_to_dict(instances_list, "InstanceId")

        return self.ec2_instance_cache.get_multiple(instance_ids, uncached_fetch,)

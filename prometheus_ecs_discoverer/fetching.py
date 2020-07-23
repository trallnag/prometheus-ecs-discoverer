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

    def get_cluster_arns(self) -> List[str]:
        """Get all cluster ARNs.

        [Boto3 API Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.list_clusters)
        """

        logger.info("Fetch all cluster ARNs.")
        arns = []
        for page in self.ecs.get_paginator("list_clusters").paginate():
            REQUESTS.labels("list_clusters").inc()
            arns += page.get("clusterArns", [])
        return arns

    def get_task_arns(self, cluster_arn: str, launch_type: str) -> List[str]:
        """Get all running task ARNs for given cluster ARN and launch type.

        :param launch_type: (EC2|FARGATE).
        
        [Boto3 API Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.list_tasks)
        """

        logger.info(f"Fetch launch_type='{launch_type}' tasks cluster='{cluster_arn}'.")
        arns = []
        for page in self.ecs.get_paginator("list_tasks").paginate(
            cluster=cluster_arn, launchType=launch_type, desiredStatus="RUNNING"
        ):
            REQUESTS.labels("list_tasks").inc()
            arns += page["taskArns"]
        return arns

    def get_tasks(self, cluster_arn: str, task_arns: List[str] = None) -> Dict[str, dict]:
        """Get task descriptions.

        :param task_arns: Defaults to `None`. This will trigger this method to 
            fetch the task ARNs for the given cluster.
        :return: Dictionary. Every entry represents a task.
        
        [Boto3 API Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.describe_tasks)
        """

        def uncached_fetch(task_arns: List[str]) -> Dict[str, dict]:
            tasks = []
            chunked_task_arns = toolbox.chunk_list(task_arns, 5)

            for task_arns_chunk in chunked_task_arns:
                tasks += self.ecs.describe_tasks(
                    cluster=cluster_arn, tasks=task_arns_chunk
                )["tasks"]
                REQUESTS.labels("describe_tasks").inc()

            return toolbox.list_to_dict(tasks, "taskArn")

        if task_arns is None:
            task_arns = []
            task_arns += self.get_task_arns(cluster_arn, "FARGATE")
            task_arns += self.get_task_arns(cluster_arn, "EC2")

        return self.task_cache.get(
            allowed_keys=task_arns, fetch_missing_data=uncached_fetch
        )

    def get_task_definition_arns(self, status: str = "ACTIVE") -> List[str]:
        """Get task definition ARNs.

        :param status: (ACTIVE|INACTIVE). Defaults to "ACTIVE".
        
        [Boto3 API Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.list_task_definitionss)
        """

        arns = []
        for page in self.ecs.get_paginator("list_task_definitions").paginate(
            status=status
        ):
            REQUESTS.labels("list_task_definitions").inc()
            arns += page["taskDefinitionArns"]
        return arns

    def get_task_definitions(
        self, task_definition_arns: List[str] = None
    ) -> Dict[str, dict]:
        """Get task definition descriptions.
        
        :param task_definition_arns: ARNs of task definitions to retrieve. 
            Defaults to `None`. In this case, both `ACTIVE` and `INACTIVE` 
            task definitions will be returned.
        :return: Dictionary wher every entry represents a task definition 
            description. Keys are the respective ARNs.

        [Boto3 API Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.describe_task_definition)
        """

        def uncached_fetch(task_definition_arns: List[str],) -> Dict[str, dict]:
            descriptions = {}
            for arn in task_definition_arns:
                response = self.ecs.describe_task_definition(taskDefinition=arn)
                REQUESTS.labels("ecs", "describe_task_definition").inc()
                response_arn = response["taskDefinition"]["taskDefinitionArn"]
                descriptions[response_arn] = response["taskDefinition"]

            return descriptions

        if task_definition_arns is None:
            task_definition_arns = []
            task_definition_arns += self.get_task_definition_arns("ACTIVE")
            task_definition_arns += self.get_task_definition_arns("INACTIVE")

        return self.task_definition_cache.get(
            allowed_keys=task_definition_arns, fetch_missing_data=uncached_fetch,
        )

    def get_container_instance_arns(self, cluster_arn: str) -> List[str]:
        """Get container instance ARNs.
        
        [Boto3 API Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ecs.html#ECS.Client.list_container_instances)
        """

        arns = []
        for page in self.ecs.get_paginator("list_container_instances").paginate(
            cluster=cluster_arn
        ):
            REQUESTS.labels("ecs", "list_container_instances").inc()
            arns += page["containerInstanceArns"]
        return arns

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
                REQUESTS.labels("ecs", "describe_container_instances").inc()

            return toolbox.list_to_dict(lst, "containerInstanceArn")

        if container_instance_arns is None:
            container_instance_arns = self.get_container_instance_arns(cluster_arn)

        return self.container_instance_cache.get(
            allowed_keys=container_instance_arns, fetch_missing_data=uncached_fetch,
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
                REQUESTS.labels("ec2", "describe_instances").inc()

            return toolbox.list_to_dict(instances_list, "InstanceId")

        return self.ec2_instance_cache.get(
            allowed_keys=instance_ids, fetch_missing_data=uncached_fetch,
        )

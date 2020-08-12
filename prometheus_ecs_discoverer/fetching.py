import time
from timeit import default_timer

from loguru import logger

from prometheus_ecs_discoverer import s, telemetry, toolbox
from prometheus_ecs_discoverer.caching import SlidingCache

# Copyright 2018, 2019 Signal Media Ltd. Licensed under the Apache License 2.0
# Modifications Copyright 2020 Tim Schwenke. Licensed under the Apache License 2.0

# Telemetry ====================================================================

CLUSTERS = telemetry.gauge("clusters", "Fetched clusters.")
CINSTANCES = telemetry.gauge(
    "container_instances", "Fetched container instances.", ("cluster",)
)
TASKS = telemetry.gauge("tasks", "Fetched tasks.", ("cluster",))
DURATION = telemetry.histogram(
    "api_requests_duration_seconds", "Duration of requests to the AWS API.", ("method",)
)

# ==============================================================================


class CachedFetcher:
    """Works with the AWS API and leverages a sliding cache.

    Reduces the amount of request made to the AWS API helping to stay below the 
    request limits. Only implements necessary methods. So not a generic class.

    Rember to flush all caches with `flush_caches()` after every "full round".
    """

    def __init__(
        self,
        ecs_client,
        ec2_client,
        throttle_interval_seconds: float = 0.1,
        should_throttle: bool = False,
    ):
        """
        :param ecs_client: Boto3 ECS client.
        :param ec2_client: Boto3 EC2 client.
        :param throttle_interval_seconds: Time to sleep after every single 
            request made to the AWS API.
        :param should_throttle: If process should go to sleep after a request 
            made to the AWS API.
        """

        self.ecs = ecs_client
        self.ec2 = ec2_client
        self.throttle_interval_seconds = throttle_interval_seconds
        self.should_throttle = should_throttle

        self.task_cache = SlidingCache(name="task_cache")
        self.task_definition_cache = SlidingCache(name="task_definition_cache")
        self.container_instance_cache = SlidingCache(name="container_instance_cache")
        self.ec2_instance_cache = SlidingCache(name="ec2_instance_cache")

    def flush_caches(self) -> None:
        self.task_cache.flush()
        self.task_definition_cache.flush()
        self.container_instance_cache.flush()
        self.ec2_instance_cache.flush()

    # ==========================================================================

    def get_arns(self, method: str, key: str, **aws_api_parameters) -> list:
        arns = []

        total_start_time = default_timer()
        start_time = total_start_time

        for page in self.ecs.get_paginator(method).paginate(**aws_api_parameters):
            DURATION.labels(method).observe(max(default_timer() - start_time, 0))
            arns += page.get(key, [])

            if self.should_throttle:
                time.sleep(self.throttle_interval_seconds)

            start_time = default_timer()

        if s.DEBUG:
            logger.bind(**aws_api_parameters).debug("{} {}.", method, key)
        if s.PRINT_STRUCTS:
            toolbox.pstruct(arns, f"{key} {method}")

        return arns

    def get_cluster_arns(self) -> list:
        arns = self.get_arns("list_clusters", "clusterArns")
        CLUSTERS.set(len(arns))
        return arns

    def get_container_instance_arns(self, cluster_arn: str) -> list:
        arns = self.get_arns(
            "list_container_instances", "containerInstanceArns", cluster=cluster_arn
        )
        CINSTANCES.labels(cluster_arn).set(len(arns))
        return arns

    def get_task_definition_arns(self) -> list:
        return self.get_arns("list_task_definitions", "taskDefinitionArns")

    def get_task_arns(self, cluster_arn: str) -> list:
        arns = self.get_arns("list_tasks", "taskArns", cluster=cluster_arn)
        TASKS.labels(cluster_arn).set(len(arns))
        return arns

    # ==========================================================================

    def get_tasks(self, cluster_arn: str, task_arns: list = None) -> dict:
        def uncached_fetch(task_arns: list) -> dict:
            logger.bind(cluster_arn=cluster_arn, task_arns=task_arns).debug(
                "Fetch tasks from AWS with describe_tasks."
            ) if s.DEBUG else None

            tasks = []
            chunked_task_arns = toolbox.chunk_list(task_arns, 100)

            for task_arns_chunk in chunked_task_arns:
                start_time = default_timer()
                tasks += self.ecs.describe_tasks(
                    cluster=cluster_arn, tasks=task_arns_chunk
                )["tasks"]
                DURATION.labels("describe_tasks").observe(
                    max(default_timer() - start_time, 0)
                )

                if self.should_throttle:
                    time.sleep(self.throttle_interval_seconds)

            if s.PRINT_STRUCTS:
                toolbox.pstruct(tasks, "describe_tasks")

            return toolbox.list_to_dict(tasks, "taskArn")

        if task_arns is None:
            task_arns = self.get_task_arns(cluster_arn)

        return self.task_cache.get_multiple(task_arns, uncached_fetch)

    def get_task_definition(self, arn: str) -> dict:
        def uncached_fetch(arn: str) -> dict:
            logger.bind(arn=arn).debug(
                "Fetch task definition from AWS with describe_task_definition."
            ) if s.DEBUG else None

            start_time = default_timer()
            task_definition = self.ecs.describe_task_definition(taskDefinition=arn)[
                "taskDefinition"
            ]
            DURATION.labels("describe_task_definition").observe(
                max(default_timer() - start_time, 0)
            )

            if s.PRINT_STRUCTS:
                toolbox.pstruct(task_definition, "fetched task definition")

            if self.should_throttle:
                time.sleep(self.throttle_interval_seconds)

            return task_definition

        return self.task_definition_cache.get_single(arn, uncached_fetch)

    def get_task_definitions(self, arns: list = None) -> dict:
        def uncached_fetch(arns: list) -> dict:
            logger.bind(arns=arns).debug(
                "Fetch task definitions from AWS with describe_task_definition."
            ) if s.DEBUG else None

            descriptions = {}
            for arn in arns:
                start_time = default_timer()
                response = self.ecs.describe_task_definition(taskDefinition=arn)
                DURATION.labels("describe_task_definition").observe(
                    max(default_timer() - start_time, 0)
                )
                response_arn = response["taskDefinition"]["taskDefinitionArn"]
                descriptions[response_arn] = response["taskDefinition"]

                if self.should_throttle:
                    time.sleep(self.throttle_interval_seconds)

            if s.PRINT_STRUCTS:
                toolbox.pstruct(descriptions, "fetched task definitions")

            return descriptions

        if arns is None:
            arns = self.get_task_definition_arns()

        return self.task_definition_cache.get_multiple(arns, uncached_fetch,)

    def get_container_instances(self, cluster_arn: str, arns: list = None) -> dict:
        def uncached_fetch(arns: list) -> dict:
            logger.bind(arns=arns).debug(
                "Fetch container instances from AWS with describe_container_instances."
            ) if s.DEBUG else None

            lst = []
            arns_chunks = toolbox.chunk_list(arns, 100)

            for arns_chunk in arns_chunks:
                start_time = default_timer()
                lst += self.ecs.describe_container_instances(
                    cluster=cluster_arn, containerInstances=arns_chunk
                )["containerInstances"]
                DURATION.labels("describe_container_instances").observe(
                    max(default_timer() - start_time, 0)
                )

                if self.should_throttle:
                    time.sleep(self.throttle_interval_seconds)

            dct = toolbox.list_to_dict(lst, "containerInstanceArn")

            if s.PRINT_STRUCTS:
                toolbox.pstruct(dct, "describe_container_instances")

            return dct

        if arns is None:
            arns = self.get_container_instance_arns(cluster_arn)

        return self.container_instance_cache.get_multiple(arns, uncached_fetch,)

    def get_ec2_instances(self, instance_ids: list) -> dict:
        def uncached_fetch(instance_ids: list) -> dict:
            logger.bind(instance_ids=instance_ids).debug(
                "Fetch EC2 instances from AWS with describe_instances."
            ) if s.DEBUG else None

            instances_list = []
            ids_chunks = toolbox.chunk_list(instance_ids, 100)

            for ids_chunk in ids_chunks:
                start_time = default_timer()
                response = self.ec2.describe_instances(InstanceIds=ids_chunk)
                for reservation in response["Reservations"]:
                    instances_list += reservation["Instances"]
                DURATION.labels("describe_instances").observe(
                    max(default_timer() - start_time, 0)
                )

                if self.should_throttle:
                    time.sleep(self.throttle_interval_seconds)

            dct = toolbox.list_to_dict(instances_list, "InstanceId")

            if s.PRINT_STRUCTS:
                toolbox.pstruct(dct, "ec2.describe_instances")

            return dct

        return self.ec2_instance_cache.get_multiple(instance_ids, uncached_fetch,)

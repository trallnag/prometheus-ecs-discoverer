from typing import Type, List
from dataclasses import dataclass

import boto3

from prometheus_ecs_discoverer.fetching import CachedFetcher
from prometheus_ecs_discoverer import toolbox


@dataclass
class Target:
    cluster_name: str = None
    task_name: str = None
    task_version: int = None
    task_id: str = None
    container_id: str = None
    instance_id: str = None
    ip: str
    port: str
    metrics_path: str


@dataclass
class TaskInfo:
    task: dict
    task_definition: dict
    container_instance: dict = None
    ec2_instance: dict = None


class PrometheusEcsDiscoverer:
    def __init__(self, session: Type[boto3.Session] = None):
        self.session = session or boto3.Session()
        self.ecs_client = self.session.client("ecs")
        self.ec2_client = self.session.client("ec2")
        self.fetcher = CachedFetcher(self.ecs_client, self.ec2_client)

        self.cluster_arns = []

    def discover(self) -> List[Type[Target]]:
        targets = []

        task_infos = []  # type: List[Type[TaskInfo]]
        for cluster_arn in self.fetcher.get_cluster_arns():
            task_infos += self.discover_task_infos(cluster_arn)

        for task_info in task_infos:
            for container in task_info.task_definition["containerDefinitions"]:
                target = self.build_target(container, task_info)
                if target:
                    targets.append(target)

    def discover_task_infos(self, cluster_arn: str) -> List[Type[TaskInfo]]:
        """Discovers tasks in a cluster and extracts necessary raw data."""

        task_infos = []  # type: List[Type[TaskInfo]]

        ec2_task_arns = self.fetcher.get_task_arns(cluster_arn, "EC2")
        fargate_task_arns = self.fetcher.get_task_arns(cluster_arn, "FARGATE")

        container_instance_arns = self.fetcher.get_container_instance_arns(cluster_arn)
        container_instances = self.fetcher.get_container_instances(
            cluster_arn, container_instance_arns
        )

        ec2_instance_ids = []
        for container_instance in container_instances.values():
            ec2_instance_ids.append(container_instance["ec2InstanceId"])
        ec2_instances = self.fetcher.get_ec2_instances(ec2_instance_ids)

        tasks = self.fetcher.get_tasks(cluster_arn, ec2_task_arns + fargate_task_arns)

        for task_arn, task in tasks.items():
            task_definition_arn = task["taskDefinitionArn"]
            task_definition = self.fetcher.get_task_definition(task_definition_arn)

            container_instance = None
            ec2_instance = None
            if task["launchType"] == "EC2":
                container_instance = container_instances[task["containerInstanceArn"]]
                ec2_instance = ec2_instances[container_instance["ec2InstanceId"]]

            task_infos.append(
                TaskInfo(task, task_definition, container_instance, ec2_instance)
            )

        return task_infos

    def build_target(self, container: dict, data: Type[TaskInfo]) -> Type[Target] or None:
        """Builds target if conditions are met.

        :param container: Container definition from task definition.
        :param data: Holds all information required.
        :return: Either the `Target` or `None`.
        """

        if toolbox.extract_env_var(container, "PROMETHEUS") is None:
            return

        nolabels = toolbox.extract_env_var(container, "PROMETHEUS_NOLABELS")
        metrics_path = toolbox.extract_env_var(container, "PROMETHEUS_ENDPOINT")

        if self.has_proper_network_binding() is False:
            self.fetcher.task_cache.pop(data.task["taskArn"], "None")
            return

        port = self._extract_port(container)
        ip = self._extract_ip(container, data)

        if nolabels:
            return Target(
                ip=ip,
                port=port,
                metrics_path=metrics_path,
            )
        else:
            if "FARGATE" in task_info.task_definition.get("requiresCompatibilities", ""):
                instance_id = container_id = None
            else:
                instance_id = task_info.container_instance["ec2InstanceId"]
                container_id = extract_name(container["containerArn"])

            return Target(
                ip=ip,
                port=port,
                metrics_path=metrics_path,
                cluster_name=data.task["clusterArn"].split(":")[5].split("/")[-1],
                task_name=data.task["taskDefinitionArn"].split(":")[5].split("/")[-1],
                task_version=data.task["taskDefinitionArn"].split(":")[6],
                task_id=data.task["taskArn"].split(":")[5].split("/")[-1],
                instance_id=instance_id,
                container_id=container_id,
            )

    def _extract_port(self, container: dict) -> str:
        prom_port = toolbox.extract_env_var(container, "PROMETHEUS_PORT")
        prom_container_port = toolbox.extract_env_var(
            container, "PROMETHEUS_CONTAINER_PORT"
        )

        has_host_port_mapping = len(container.get("portMappings", [])) > 0

        if prom_port:
            port = prom_port
        elif data.task_definition.get("networkMode") in ("host", "awsvpc"):
            if has_host_port_mapping:
                port = str(container["portMappings"][0]["hostPort"])
            else:
                port = "80"
        elif prom_container_port:
            binding_by_container_port = [
                c
                for c in container["networkBindings"]
                if str(c["containerPort"]) == prom_container_port
            ]
            if binding_by_container_port:
                port = str(binding_by_container_port[0]["hostPort"])
            else:
                return
        else:
            port = str(container["networkBindings"][0]["hostPort"])
        
        return port

    def _extract_ip(self, container: dict, data: dict) -> str:
        if data.task_definition["networkMode"] == "awsvpc":
            return container["networkInterfaces"][0]["privateIpv4Address"]
        else:
            return data.ec2_instance["PrivateIpAddress"]



# from timeit import default_timer


# x = PrometheusEcsDiscoverer()

# time = default_timer()
# x.discover()
# print(default_timer() - time)

# time = default_timer()
# x.discover()
# print(default_timer() - time)

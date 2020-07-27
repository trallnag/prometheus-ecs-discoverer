from typing import Type, List, Dict
from dataclasses import dataclass
from timeit import default_timer

from loguru import logger
import boto3

from prometheus_ecs_discoverer.fetching import CachedFetcher
from prometheus_ecs_discoverer import toolbox


@dataclass
class Target:
    ip: str
    port: str
    p_instance: str
    task_name: str
    metrics_path: str = None
    cluster_name: str = None
    task_version: int = None
    task_id: str = None
    container_id: str = None
    instance_id: str = None
    custom_labels: Dict[str, str] = None


@dataclass
class TaskInfo:
    task: dict
    task_definition: dict
    container_instance: dict = None
    ec2_instance: dict = None


class PrometheusEcsDiscoverer:
    def __init__(
        self, session: Type[boto3.Session] = None, ecs_client=None, ec2_client=None
    ):
        if ecs_client and ec2_client:
            self.ecs_client = ecs_client
            self.ec2_client = ec2_client
        else:
            self.session = session or boto3.Session()
            self.ecs_client = self.session.client("ecs")
            self.ec2_client = self.session.client("ec2")
        self.fetcher = CachedFetcher(self.ecs_client, self.ec2_client)
        logger.info("Initialized discoverer and required boto3 clients.")

    def discover(self) -> List[Type[Target]]:
        start_time = default_timer()

        targets = []

        task_infos = []  # type: List[Type[TaskInfo]]
        for cluster_arn in self.fetcher.get_cluster_arns():
            task_infos += self._discover_task_infos(cluster_arn)

        for task_info in task_infos:
            for container in task_info.task["containers"]:
                target = self._build_target(container, task_info)
                if target:
                    targets.append(target)

        duration = max(default_timer() - start_time, 0)
        logger.bind(duration=duration).info("Discovered {} targets.", len(targets))

        self.fetcher.flush_caches()
        return targets

    def _discover_task_infos(self, cluster_arn: str) -> List[Type[TaskInfo]]:
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
            if task.get("launchType") != "FARGATE":
                container_instance = container_instances[task["containerInstanceArn"]]
                ec2_instance = ec2_instances[container_instance["ec2InstanceId"]]

            task_infos.append(
                TaskInfo(task, task_definition, container_instance, ec2_instance)
            )

        logger.bind(
            cluster=cluster_arn,
            ec2_tasks=len(ec2_task_arns),
            fargate_tasks=len(fargate_task_arns),
            container_instances=len(container_instance_arns),
            ec2_instances=len(ec2_instances),
        ).info("Discovered {} task infos.", len(task_infos))

        return task_infos

    def _build_target(
        self, container: dict, data: Type[TaskInfo]
    ) -> Type[Target] or None:
        """Builds target if conditions are met.

        :param container: Container from task. Not the continer definition.
        :param data: Holds all information required.
        :return: Either the `Target` or `None`.
        """

        if PRINT_STRUCTURES:
            ps(data.task, "task")
            ps(data.task_definition, "task_definition")
            ps(data.container_instance, "container_instance")
            ps(data.ec2_instance, "ec2_instance")

        container_name = container["name"]
        task_definition_arn = data.task["taskDefinitionArn"]
        task_arn = data.task["taskArn"]

        _logger = logger.bind(
            container=container_name, task_definition=task_definition_arn, task=task_arn,
        )

        for defi in data.task_definition["containerDefinitions"]:
            if container_name == defi["name"]:
                container_definition = defi

        if toolbox.extract_env_var(container_definition, "PROMETHEUS") is None:
            _logger.debug("Prometheus env var not found. Reject container.")
            return

        metrics_path = toolbox.extract_env_var(
            container_definition, "PROMETHEUS_ENDPOINT"
        )

        if not _has_proper_network_binding(container, data):
            _logger.warning(
                (
                    "Container marked as Prometheus target, but it has no "
                    "proper network binding. Reject container and remove task "
                    "from cache."
                )
            )
            self.fetcher.task_cache.current.pop(task_arn, None)
            return

        port = _extract_port(container, data)
        ip = _extract_ip(container, data)

        custom_labels = _extract_custom_labels(container_definition)

        task_name = data.task["taskDefinitionArn"].split(":")[5].split("/")[-1]

        if toolbox.extract_env_var(container_definition, "PROMETHEUS_NOLABELS"):
            target = Target(
                ip=ip,
                port=port,
                metrics_path=metrics_path,
                p_instance=task_name,
                task_name=task_name,
                custom_labels=custom_labels,
            )
            logger.bind(
                ip=target.ip,
                port=target.port,
                metrics_path=target.metrics_path,
                custom_labels=custom_labels,
            ).info("Build target successfully from discovered task info.")
            return target

        if "FARGATE" in data.task_definition.get("requiresCompatibilities", ""):
            instance_id = container_id = None
        else:
            instance_id = data.container_instance["ec2InstanceId"]
            container_id = container["containerArn"].split(":")[5].split("/")[-1]

        target = Target(
            ip=ip,
            port=port,
            metrics_path=metrics_path,
            cluster_name=data.task["clusterArn"].split(":")[5].split("/")[-1],
            task_name=data.task["taskDefinitionArn"].split(":")[5].split("/")[-1],
            task_version=data.task["taskDefinitionArn"].split(":")[6],
            task_id=data.task["taskArn"].split(":")[5].split("/")[-1],
            p_instance=f"{ip}:{port}",
            instance_id=instance_id,
            container_id=container_id,
            custom_labels=custom_labels,
        )

        logger.bind(
            ip=target.ip,
            port=target.port,
            metrics_path=target.metrics_path,
            cluster_name=target.cluster_name,
            task_name=target.task_name,
            task_version=target.task_version,
            task_id=target.task_id,
            instance_id=target.instance_id,
            container_id=target.container_id,
            custom_labels=custom_labels,
        ).info("Build target successfully from discovered task info.")

        return target


def _extract_port(container: dict, data: dict) -> str:
    prom_port = toolbox.extract_env_var(container, "PROMETHEUS_PORT")
    prom_container_port = toolbox.extract_env_var(container, "PROMETHEUS_CONTAINER_PORT")

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


def _extract_ip(container: dict, data: dict) -> str:
    if data.task_definition.get("networkMode") == "awsvpc":
        return container["networkInterfaces"][0]["privateIpv4Address"]
    else:
        return data.ec2_instance["PrivateIpAddress"]


def _has_proper_network_binding(container: dict, data: Type[TaskInfo]) -> bool:
    if (
        len(container.get("networkBindings", [])) > 0
        or len(container.get("networkInterfaces", [])) > 0
    ):
        return True

    is_host_network_mode = data.task_definition.get("networkMode") == "host"
    prom_port = toolbox.extract_env_var(container, "PROMETHEUS_PORT")
    port_mappings = container["portMappings"]

    if not (is_host_network_mode and (prom_port or port_mappings)):
        ps(container, "container") if PRINT_STRUCTURES else None
        return False

    return True


def _extract_custom_labels(container_definition: dict) -> Dict[str, str]:
    labels = {}
    for envvar in container_definition.get("environment", []):
        name = envvar["name"]
        if name.startswith("PROMETHEUS_LABEL_"):
            labels[name[17:]] = envvar["value"]
    return labels

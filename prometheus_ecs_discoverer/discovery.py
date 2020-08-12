from dataclasses import dataclass
from typing import Dict, List, Type

from loguru import logger

from prometheus_ecs_discoverer import s, telemetry, toolbox
from prometheus_ecs_discoverer.fetching import CachedFetcher

# Copyright 2018, 2019 Signal Media Ltd. Licensed under the Apache License 2.0
# Modifications Copyright 2020 Tim Schwenke. Licensed under the Apache License 2.0


# ==============================================================================
# Telemetry

TASK_INFOS = telemetry.gauge("task_infos", "Discovered and built task infos.")
TARGETS = telemetry.gauge("targets", "Discovered and built targets.")
TDEFINITIONS = telemetry.gauge("task_definitions", "Fetched task definitions.")

# ==============================================================================


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
    def __init__(self, fetcher: Type[CachedFetcher]):
        self.fetcher = fetcher

    def discover(self) -> List[Type[Target]]:
        targets = []

        task_infos = []
        for cluster_arn in self.fetcher.get_cluster_arns():
            task_infos += self._discover_task_infos(cluster_arn)
        TASK_INFOS.set(len(task_infos))

        for task_info in task_infos:
            for container in task_info.task["containers"]:
                target = self._build_target(container, task_info)
                if target:
                    targets.append(target)

        TARGETS.set(len(targets))
        logger.info("Discovered {} targets.", len(targets))

        self.fetcher.flush_caches()
        return targets

    def _discover_task_infos(self, cluster_arn: str) -> List[Type[TaskInfo]]:
        """Discovers tasks in a cluster and extracts necessary raw data."""

        task_infos = []  # type: List[Type[TaskInfo]]

        task_arns = self.fetcher.get_task_arns(cluster_arn)

        container_instance_arns = self.fetcher.get_container_instance_arns(cluster_arn)
        container_instances = self.fetcher.get_container_instances(
            cluster_arn, container_instance_arns
        )

        ec2_instance_ids = []
        for container_instance in container_instances.values():
            ec2_instance_ids.append(container_instance["ec2InstanceId"])
        ec2_instances = self.fetcher.get_ec2_instances(ec2_instance_ids)

        tasks = self.fetcher.get_tasks(cluster_arn, task_arns)

        task_definition_arns = set()

        for task_arn, task in tasks.items():
            task_definition_arn = task["taskDefinitionArn"]
            task_definition_arns.add(task_definition_arn)
            task_definition = self.fetcher.get_task_definition(task_definition_arn)

            container_instance = None
            ec2_instance = None
            if task.get("launchType") != "FARGATE":
                container_instance = container_instances[task["containerInstanceArn"]]
                ec2_instance = ec2_instances[container_instance["ec2InstanceId"]]

            task_infos.append(
                TaskInfo(task, task_definition, container_instance, ec2_instance)
            )

        TDEFINITIONS.set(len(task_definition_arns))

        logger.bind(
            cluster=cluster_arn,
            tasks=len(task_arns),
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
            _logger.debug("Prometheus env var NOT found. Reject container.")
            return
        else:
            _logger.debug("Prometheus env var found. Build target.")

        metrics_path = toolbox.extract_env_var(
            container_definition, "PROMETHEUS_ENDPOINT"
        )
        prom_port = toolbox.extract_env_var(container_definition, "PROMETHEUS_PORT")

        network_bindings = container.get("networkBindings", [])
        network_interfaces = container.get("networkInterfaces", [])
        network_mode = data.task_definition.get("networkMode", "bridge")
        port_mappings = container_definition.get("portMappings", [])

        if not _has_proper_network(
            network_bindings,
            network_interfaces,
            network_mode,
            prom_port,
            port_mappings,
            _logger,
        ):
            self.fetcher.task_cache.current.pop(task_arn, None)
            return

        port = _extract_port(
            network_mode,
            prom_port,
            toolbox.extract_env_var(container, "PROMETHEUS_CONTAINER_PORT"),
            port_mappings,
            network_bindings,
        )
        if port is None:
            _logger.warning("Does not expose port matching PROMETHEUS_CONTAINER_PORT.")
            return

        ip = _extract_ip(network_mode, network_interfaces, data.ec2_instance)

        custom_labels = _extract_custom_labels(
            env=container_definition.get("environment", [])
        )

        task_name = data.task["taskDefinitionArn"].split(":")[5].split("/")[-1]

        if toolbox.extract_env_var(container_definition, "PROMETHEUS_NOLABELS"):
            _logger.debug("Build target successfully from discovered task info.")

            return Target(
                ip=ip,
                port=port,
                metrics_path=metrics_path,
                p_instance=task_name,
                task_name=task_name,
                custom_labels=custom_labels,
            )

        if "FARGATE" in data.task_definition.get("requiresCompatibilities", ""):
            instance_id = container_id = None
        else:
            instance_id = data.container_instance["ec2InstanceId"]
            container_id = container["containerArn"].split(":")[5].split("/")[-1]

        _logger.debug("Build target successfully from discovered task info.")

        return Target(
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


def _extract_port(
    network_mode: str,
    prom_port,
    prom_container_port,
    port_mappings: list,
    network_bindings: list,
) -> str or None:
    if prom_port:
        return prom_port

    if network_mode in ("host", "awsvpc"):
        if len(port_mappings) > 0:
            return str(port_mappings[0]["hostPort"])
        else:
            return "80"

    if prom_container_port:
        binding_by_container_port = [
            c for c in network_bindings if str(c["containerPort"]) == prom_container_port
        ]
        if binding_by_container_port:
            return str(binding_by_container_port[0]["hostPort"])
        else:
            return None

    return str(network_bindings[0]["hostPort"])


def _extract_ip(network_mode: str, network_interfaces: list, ec2_instance: dict) -> str:
    if network_mode == "awsvpc":
        return network_interfaces[0]["privateIpv4Address"]
    else:
        return ec2_instance["PrivateIpAddress"]


def _has_proper_network(
    network_bindings: list,
    network_interfaces: list,
    network_mode: str,
    prom_port: str or None,
    port_mappings: list,
    scoped_logger,
) -> bool:
    if len(network_bindings) > 0 or len(network_interfaces) > 0:
        return True

    if network_mode == "host" and (prom_port or port_mappings):
        return True

    scoped_logger.bind(
        len_network_bindings=len(network_bindings),
        len_network_interfaces=len(network_interfaces),
        network_mode=network_mode,
        prom_port=bool(prom_port),
        port_mappings=bool(port_mappings),
    ).warning("Has no network binding.")

    return False


def _extract_custom_labels(env: List[Dict[str, str]] or List) -> Dict[str, str]:
    labels = {}
    for envvar in env:
        name = envvar["name"]
        if name.startswith(s.CUSTOM_LABEL_PREFIX):
            labels[name[len(s.CUSTOM_LABEL_PREFIX) :].lower()] = envvar["value"]
    return labels

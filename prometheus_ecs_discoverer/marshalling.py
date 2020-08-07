import json
import os
import re
from typing import Dict, List, Type

from loguru import logger

from prometheus_ecs_discoverer import s
from prometheus_ecs_discoverer.discovery import Target

# Copyright 2018, 2019 Signal Media Ltd. Licensed under the Apache License 2.0
# Modifications Copyright 2020 Tim Schwenke. Licensed under the Apache License 2.0


def _extract_path_interval_pairs(metrics_path: str = None,) -> Dict[str, str or None]:
    """Extracts path intervals from given metrics path.

    Transforms a string like this `30s:/mymetrics1,/mymetrics2` into:

    ```
    {
        "/mymetrics1": "30s",
        "/mymetrics2": None
    }
    ```
    """

    if not metrics_path:
        return {s.FALLBACK_METRICS_ENDPOINT: None}

    path_interval = {}

    for entry in metrics_path.split(","):
        if ":" in entry:
            pi = entry.split(":")
            if re.search("(15s|30s|1m|5m)", pi[0]):
                path_interval[pi[1]] = pi[0]
            else:
                path_interval[pi[1]] = None
        else:
            path_interval[entry] = None

    logger.bind(inp=metrics_path, outp=path_interval).debug(
        "Extracted path interval pairs."
    ) if s.DEBUG else None

    return path_interval


def _get_filename(
    interval: str or None = None,
    filename_15s: str = s.FILENAME_15S,
    filename_30s: str = s.FILENAME_30S,
    filename_1m: str = s.FILENAME_1M,
    filename_5m: str = s.FILENAME_5M,
    filename_generic: str = s.FILENAME_GENERIC,
) -> str:
    if interval == "15s":
        return filename_15s
    elif interval == "30s":
        return filename_30s
    elif interval == "1m":
        return filename_1m
    elif interval == "5m":
        return filename_5m
    else:
        return filename_generic


def _marshall_targets(
    targets: List[Type[Target]],
    filename_15s: str = s.FILENAME_15S,
    filename_30s: str = s.FILENAME_30S,
    filename_1m: str = s.FILENAME_1M,
    filename_5m: str = s.FILENAME_5M,
    filename_generic: str = s.FILENAME_GENERIC,
    labelname_cluster: str = s.LABELNAME_CLUSTER,
    labelname_taskversion: str = s.LABELNAME_TASKVERSION,
    labelname_taskid: str = s.LABELNAME_TASKID,
    labelname_containerid: str = s.LABELNAME_CONTAINERID,
    labelname_instanceid: str = s.LABELNAME_INSTANCEID,
) -> Dict[str, List[Dict]]:
    """Marshalls given targets into JSON compatible structure.

    ```
    {
        "tasks.json": [
            {
                "targets": [
                    "ip:port"
                ],
                "labels": {
                    "instance": "ip:port",
                    "job": "job",
                    "and": "more"
                },
            },
            ...
        ],
        "15s-tasks.json": [
            ...
        ],
        "30s-tasks.json": [
            ...
        ],
        "1m-tasks.json": [
            ...
        ],
        "5m-tasks.json": [
            ...
        ]
    }
    ```
    """

    result = {
        s.FILENAME_GENERIC: [],
        s.FILENAME_15S: [],
        s.FILENAME_30S: [],
        s.FILENAME_1M: [],
        s.FILENAME_5M: [],
    }

    for target in targets:
        path_interval_pairs = _extract_path_interval_pairs(target.metrics_path)
        for path, interval in path_interval_pairs.items():
            labels = {}

            if target.custom_labels:
                labels.update(target.custom_labels)

            labels["instance"] = target.p_instance
            labels["job"] = target.task_name
            labels["metrics_path"] = path

            if target.cluster_name:
                labels[labelname_cluster] = target.cluster_name
            if target.task_version:
                labels[labelname_taskversion] = target.task_version
            if target.task_id:
                labels[labelname_taskid] = target.task_id
            if target.container_id:
                labels[labelname_containerid] = target.container_id
            if target.instance_id:
                labels[labelname_instanceid] = target.instance_id

            job = {"targets": [f"{target.ip}:{target.port}"], "labels": labels}

            result[_get_filename(interval)].append(job)

    logger.bind(**result).info("Marshalled targets")

    return result


def write_targets_to_file(targets: List[Type[Target]], output_directory: str) -> None:
    if not os.path.isdir(output_directory):
        raise OSError(f"Directory '{output_directory}' not found.")

    for file_name, content in _marshall_targets(targets).items():
        file_path = f"{output_directory}/{file_name}"
        tmp_file_path = f"{file_path}.tmp"
        with open(tmp_file_path, "w") as file:
            file.write(json.dumps(content, indent=4))
        os.rename(tmp_file_path, file_path)
        logger.bind(file=file_path).debug("Written file.") if s.DEBUG else None

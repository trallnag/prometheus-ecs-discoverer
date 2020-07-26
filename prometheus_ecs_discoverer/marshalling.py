from typing import List, Type, Tuple
import os
import json

from loguru import logger

from prometheus_ecs_discoverer.discovery import Target
from prometheus_ecs_discoverer import toolbox, settings


def _extract_path_interval_pairs(
    metrics_path: str = None,
) -> Dict[Tuple[str, str or None]]:
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
        return {settings.FALLBACK_METRICS_ENDPOINT: None}

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
    ) if settings.LOG_LEVEL == settings.DEBUG else None

    return path_interval


def marshall_targets(
    targets: List[Type[Target]],
    filename_generic: str = settings.FILENAME_GENERIC_JOBS,
    filename_15s: str = settings.FILENAME_15S_JOBS,
    filename_30s: str = settings.FILENAME_30S_JOBS,
    filename_1m: str = settings.FILENAME_1M_JOBS,
    filename_5m: str = settings.FILENAME_5M_JOBS,
) -> Dict[List[Dict]]:
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
        filename_generic: [],
        filename_15s: [],
        filename_30s: [],
        filename_1m: [],
        filename_5m: [],
    }

    for target in targets:
        path_interval_pairs = _extract_path_interval_pairs(target.metrics_path)
        for path, interval in path_interval_pairs.items():
            labels = {}

            labels.update(target.custom_labels)

            labels["instance"] = target.p_instance
            labels["job"] = target.task_name
            labels["metrics_path"] = path

            labels["cluster"] = target.cluster_name if target.cluster_name else None
            labels["task_version"] = target.task_version if target.task_version else None
            labels["task_id"] = target.task_id if target.task_id else None
            labels["container_id"] = target.container_id if target.container_id else None
            labels["instance_id"] = target.instance_id if target.instance_id else None

            job = {"targets": [f"{target.ip}:{target.port}"], "labels": labels}

            if interval == "15s":
                result[filename_15s].append(job)
            elif interval == "30s":
                result[filename_30s].append(job)
            elif interval == "1m":
                result[filename_1m].append(job)
            elif interval == "5m":
                result[filename_5m].append(job)
            else:
                result[filename_generic].append(job)

    toolbox.pstruct(result) if settings.PRINT_STRUCTS else None


def write_targets_to_file(
    result: Dict[List[Dict]], output_directory: str = settings.OUTPUT_DIRECTORY
) -> None:
    for file_name, content in result.items():
        file_path = f"{output_directory}/{file_name}"
        tmp_file_path = f"{file_path}.tmp"
        with open(tmp_file_path, "w") as file:
            file.write(json.dumps(content, indent=4))
        os.rename(tmp_file_path, file_path)

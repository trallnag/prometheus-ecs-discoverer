from prometheus_ecs_discoverer import discovery, marshalling, toolbox
from prometheus_ecs_discoverer import settings as s


# ------------------------------------------------------------------------------
# extract_path_interval_pairs


def test_extract_path_interval_pairs_1():
    inp = "30s:/mymetrics1,/mymetrics2"
    outp = marshalling._extract_path_interval_pairs(inp)
    toolbox.pstruct(outp, inp)

    assert outp == {"/mymetrics1": "30s", "/mymetrics2": None}


def test_extract_path_interval_pairs_2():
    inp = "30s:/mymetrics1,5m:/mymetrics2"
    outp = marshalling._extract_path_interval_pairs(inp)
    toolbox.pstruct(outp, inp)

    assert outp == {"/mymetrics1": "30s", "/mymetrics2": "5m"}


def test_extract_path_interval_pairs_3():
    inp = None
    outp = marshalling._extract_path_interval_pairs(inp)
    toolbox.pstruct(outp, inp)

    assert outp == {"/metrics": None}


def test_extract_path_interval_pairs_4():
    inp = "31s:/mymetrics1,/mymetrics2"
    outp = marshalling._extract_path_interval_pairs(inp)
    toolbox.pstruct(outp, inp)

    assert outp == {"/mymetrics1": None, "/mymetrics2": None}


# ------------------------------------------------------------------------------
# marshall_targets


def test_marshalling_targets_intervals():
    targets = [
        discovery.Target(
            ip="ip",
            port="port",
            p_instance="task_name",
            task_name="task_name",
            metrics_path=None,
        ),
        discovery.Target(
            ip="ip",
            port="port",
            p_instance="task_name",
            task_name="task_name",
            metrics_path="/mymetrics2",
        ),
        discovery.Target(
            ip="ip",
            port="port",
            p_instance="task_name",
            task_name="task_name",
            metrics_path="15s:/mymetrics,/metrics",
        ),
        discovery.Target(
            ip="ip",
            port="port",
            p_instance="task_name",
            task_name="task_name",
            metrics_path="30s:/mymetrics",
        ),
        discovery.Target(
            ip="ip",
            port="port",
            p_instance="task_name",
            task_name="task_name",
            metrics_path="1m:/mymetrics",
        ),
        discovery.Target(
            ip="ip",
            port="port",
            p_instance="task_name",
            task_name="task_name",
            metrics_path="5m:/mymetrics",
        ),
    ]

    result = marshalling.marshall_targets(targets)
    toolbox.pstruct(result, "result marshall_targets")

    assert result == {
        s.marshalling.filename_generic: [
            {
                "targets": ["ip:port"],
                "labels": {
                    "instance": "task_name",
                    "job": "task_name",
                    "metrics_paths": "/metrics",
                },
            },
            {
                "targets": ["ip:port"],
                "labels": {
                    "instance": "task_name",
                    "job": "task_name",
                    "metrics_paths": "/mymetrics2",
                },
            },
            {
                "targets": ["ip:port"],
                "labels": {
                    "instance": "task_name",
                    "job": "task_name",
                    "metrics_paths": "/metrics",
                },
            },
        ],
        s.marshalling.filename_15s: [
            {
                "targets": ["ip:port"],
                "labels": {
                    "instance": "task_name",
                    "job": "task_name",
                    "metrics_paths": "/mymetrics",
                },
            },
        ],
        s.marshalling.filename_30s: [
            {
                "targets": ["ip:port"],
                "labels": {
                    "instance": "task_name",
                    "job": "task_name",
                    "metrics_paths": "/mymetrics",
                },
            },
        ],
        s.marshalling.filename_1m: [
            {
                "targets": ["ip:port"],
                "labels": {
                    "instance": "task_name",
                    "job": "task_name",
                    "metrics_paths": "/mymetrics",
                },
            },
        ],
        s.marshalling.filename_5m: [
            {
                "targets": ["ip:port"],
                "labels": {
                    "instance": "task_name",
                    "job": "task_name",
                    "metrics_paths": "/mymetrics",
                },
            },
        ],
    }

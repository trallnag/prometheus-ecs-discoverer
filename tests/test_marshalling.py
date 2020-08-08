import os

from prometheus_ecs_discoverer import s, discovery, marshalling
from prometheus_ecs_discoverer import toolbox

# ------------------------------------------------------------------------------
# _extract_path_interval_pairs


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
# _get_filename


def test_get_filename_defaults():
    assert marshalling._get_filename() == s.FILENAME_GENERIC
    assert marshalling._get_filename(interval="15s") == s.FILENAME_15S
    assert marshalling._get_filename(interval="30s") == s.FILENAME_30S
    assert marshalling._get_filename(interval="1m") == s.FILENAME_1M
    assert marshalling._get_filename(interval="5m") == s.FILENAME_5M


def test_get_filename_custom():
    assert marshalling._get_filename(interval="15s", filename_15s="test") == "test"


# ------------------------------------------------------------------------------
# marshall_targets


def test_marshalling_targets_nolabels():
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

    result = marshalling._marshall_targets(targets)

    expected = {
        s.FILENAME_GENERIC: [
            {
                "targets": ["ip:port"],
                "labels": {
                    "instance": "task_name",
                    "job": "task_name",
                    "metrics_path": "/metrics",
                },
            },
            {
                "targets": ["ip:port"],
                "labels": {
                    "instance": "task_name",
                    "job": "task_name",
                    "metrics_path": "/mymetrics2",
                },
            },
            {
                "targets": ["ip:port"],
                "labels": {
                    "instance": "task_name",
                    "job": "task_name",
                    "metrics_path": "/metrics",
                },
            },
        ],
        s.FILENAME_15S: [
            {
                "targets": ["ip:port"],
                "labels": {
                    "instance": "task_name",
                    "job": "task_name",
                    "metrics_path": "/mymetrics",
                },
            },
        ],
        s.FILENAME_30S: [
            {
                "targets": ["ip:port"],
                "labels": {
                    "instance": "task_name",
                    "job": "task_name",
                    "metrics_path": "/mymetrics",
                },
            },
        ],
        s.FILENAME_1M: [
            {
                "targets": ["ip:port"],
                "labels": {
                    "instance": "task_name",
                    "job": "task_name",
                    "metrics_path": "/mymetrics",
                },
            },
        ],
        s.FILENAME_5M: [
            {
                "targets": ["ip:port"],
                "labels": {
                    "instance": "task_name",
                    "job": "task_name",
                    "metrics_path": "/mymetrics",
                },
            },
        ],
    }
    toolbox.pstruct(expected, "expected")
    assert result == expected


def test_marshalling_targets_labels():
    targets = [
        discovery.Target(
            ip="ip",
            port="port",
            p_instance="ip:port",
            task_name="task_name",
            metrics_path=None,
            cluster_name="cluster_name",
            task_version="task_version",
            task_id="task_id",
            container_id="container_id",
            instance_id="instance_id",
            custom_labels={"custom_label1": "value", "custom_label2": "value",},  # noqa
        )
    ]

    result = marshalling._marshall_targets(targets)

    expected = {
        s.FILENAME_GENERIC: [
            {
                "targets": ["ip:port"],
                "labels": {
                    "instance": "ip:port",
                    "job": "task_name",
                    "metrics_path": "/metrics",
                    "metrics_path": "/metrics",
                    "cluster": "cluster_name",
                    "task_version": "task_version",
                    "task_id": "task_id",
                    "container_id": "container_id",
                    "instance_id": "instance_id",
                    "custom_label1": "value",
                    "custom_label2": "value",
                },
            },
        ],
        s.FILENAME_15S: [],
        s.FILENAME_30S: [],
        s.FILENAME_1M: [],
        s.FILENAME_5M: [],
    }
    toolbox.pstruct(expected, "expected")
    assert result == expected


# ------------------------------------------------------------------------------
# write_targets_to_file


def test_write_targets_to_file(tmp_path):
    targets = [
        discovery.Target(
            ip="ip",
            port="port",
            p_instance="ip:port",
            task_name="task_name",
            metrics_path=None,
            cluster_name="cluster_name",
            task_version="task_version",
            task_id="task_id",
            container_id="container_id",
            instance_id="instance_id",
            custom_labels={"custom_label1": "value", "custom_label2": "value",},  # noqa
        )
    ]

    marshalling.write_targets_to_file(targets, tmp_path)

    assert os.path.isfile(os.path.join(tmp_path, s.FILENAME_GENERIC))
    assert os.path.isfile(os.path.join(tmp_path, s.FILENAME_15S))
    assert os.path.isfile(os.path.join(tmp_path, s.FILENAME_30S))
    assert os.path.isfile(os.path.join(tmp_path, s.FILENAME_1M))
    assert os.path.isfile(os.path.join(tmp_path, s.FILENAME_5M))

    with open(os.path.join(tmp_path, s.FILENAME_GENERIC)) as f:
        assert "task_name" in f.read()

    with open(os.path.join(tmp_path, s.FILENAME_30S)) as f:
        assert "[]" == f.readlines()[0]

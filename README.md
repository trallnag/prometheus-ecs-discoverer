# Prometheus ECS Discoverer

[![PyPI version](https://badge.fury.io/py/prometheus-ecs-discoverer.svg)](https://pypi.python.org/pypi/prometheus-ecs-discoverer/)
[![Maintenance](https://img.shields.io/badge/maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![downloads](https://img.shields.io/pypi/dm/prometheus-ecs-discoverer)](https://pypi.org/project/prometheus-ecs-discoverer/)

![release](https://github.com/trallnag/prometheus-ecs-discoverer/workflows/release/badge.svg)
![test branches](https://github.com/trallnag/prometheus-ecs-discoverer/workflows/test%20branches/badge.svg)
[![codecov](https://codecov.io/gh/trallnag/prometheus-ecs-discoverer/branch/master/graph/badge.svg)](https://codecov.io/gh/trallnag/prometheus-ecs-discoverer)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Based on [prometheus-ecs-sd](https://github.com/signal-ai/prometheus-ecs-sd), 
this project enables your Prometheus to **dynamically scrape targets** deployed 
in AWS ECS. The discoverer is perfect if you don't have 
a service discovery system like Consul in-place. It provides an easy-to-use 
alternative and can be used in low- to mid-sized environments with **hundreds 
of tasks** running in parallel.

Once the discoverer is up and running, any task can be made visible to 
Prometheus.

![diagram](https://raw.githubusercontent.com/trallnag/prometheus-ecs-discoverer/master/documents/drawio-diagram.png)

What are the advantages of using this project over [prometheus-ecs-sd](https://github.com/signal-ai/prometheus-ecs-sd
)?

* Modified throttling in combination with the already existing caching allows 
    the usage in environments with hundreds of tasks.
* Every target can expose custom labels via its environment variables. This way 
    you can provide more ways to aggregate metrics. For example by type of API.
* Deploy as container (provided and can be used directly) or Python package.
    No need to manually install boto3 and so on.
* Instrumented with Prometheus. Allows more insights into the discoverer. You 
    can monitor how long discovery rounds take and stuff like used memory. 
    Dashboard already included and ready to use.
* Extensive testing with high coverage ensures functionality.
* More configuration options. For example structured logs.

---

Contents: **[Setup](#setup)** |
[Prepare targets](#perpare-targets) | 
[Deploy PromED](#deploy-promed) |
[Configure Prometheus](#configure-prometheus) | 
**[Configuration](#configuration)** |
**[Grafana Dashboard](#grafana-dashboard)** |
**[Prerequesites](#prerequesites)** |
**[Development](#development)**

---

## Setup

As this project is based on 
[prometheus-ecs-sd](https://github.com/signal-ai/prometheus-ecs-sd), the setup 
is very similar / exactly the same. The setup consists out of three parts. 
The targets must be prepared by adding environment variables. Next, PromED 
itself must be deployed. And finally, the Prometheus configuration must be 
updated.

### Prepare targets

Targets are setup via setting environment variables in the task definitions.

#### Mark container as target

Set `PROMETHEUS_TARGET` to `true` to make PromED consider the container. This 
by itself is already enough to make it work with the configured defaults.

#### Specify metrics endpoint(s)

If your metrics are not exposed on the default `/metrics` endpoint, you can 
specifiy the endpoint with `PROMETHEUS_ENDPOINT`.

You can also declare multiple endpoints and different intervals. The supported 
intervals are `15s`, `30s`, `1m` and `5m`. Based on the interval, targets will 
end up in different files. The default interval is "generic". Examples for this:

* `5m:/mymetrics,30s:/mymetrics2`
* `/mymetrics`
* `/mymetrics,30s:/mymetrics2`

By default, all targets will end up in a single file called `tasks.json` in the 
configured directory (defaults to `/tmp`).

#### Set custom labels for container

Sometimes you might want to add additonal labels to targets to group them. 
For example by the used API type (REST vs. GraphQL). This can be done by adding 
environment variables to the container definition in the respective task 
definition with the  `PROMETHEUS_LABEL_` prefix. For example 
`PROMETHEUS_LABEL_api_type` or `PROMETHEUS_LABEL_foo`.

Environment variables set from within the container are not visible to PromED 
and are ignored.

#### Customize networking

Regarding networking, all network modes are supported (`bridge`, `host` 
and `awsvpc`).

If `PROMETHEUS_PORT` and `PROMETHEUS_CONTAINER_PORT` are not set, the script 
will pick the first port from the container definition (in awsvpc and host 
network mode) or the container host network bindings in bridge mode. On 
Fargate, if `PROMETHEUS_PORT` is not set, it will default to port `80`.
 
If `PROMETHEUS_CONTAINER_PORT` is set, it will look at the container host 
network bindings, and find the entry with a matching `containerPort`. It will 
then use the `hostPort` found there as target port. This is useful when the 
container port is known, but the `hostPort` is randomly picked by ECS (by 
setting `hostPort` to `0` in the task definition).

If your container uses multiple ports, it's recommended to specify 
`PROMETHEUS_PORT` (`awsvpc`, `host`) or `PROMETHEUS_CONTAINER_PORT` (`bridge`).

*Quoted from 
[prometheus-ecs-sd](https://github.com/signal-ai/prometheus-ecs-sd) 
commit `ece6ca2`.*

### Deploy PromED

You can either use the Python package directly or go for the Docker image. 
Please note that just running the package / image is not enough. The enviornment
must be ready for boto3. This includes credentials and approbiate rights.

#### Using package from PyPI

Available under the name `prometheus_ecs_discoverer`. To start PromED:

```sh
python -m prometheus_ecs_discoverer.run
```

To configure PromED you can either provide a settings file or use plain 
environment variables.  Please see [Configuration](#configuration) for more 
info. Please see [Configuration](#configuration) for more info.

#### Using Docker image

The image `trallnag/prometheus_ecs_discoverer` can be found 
[here](https://hub.docker.com/repository/docker/trallnag/prometheus_ecs_discoverer).
The recommended way for configuring the image is to use environment variables.

You will probably want to run the discoverer in ECS. Here, you don't have to 
provide credentials assuming everything is set up correctly. Boto3 will 
automatically detect relative credentials URI and retrieve them from AWS.
Nevertheless, the region must be set by you.

#### AWS IAM

The actions that PromED is performing on the AWS API can be found in 
[aws-iam-policy.json](https://github.com/trallnag/prometheus-ecs-discoverer/blob/master/documents/aws-iam-policy.json).
The allowed actions must be attached to an approbiate role. If you deploy 
PromED in ECS, this should look like in [aws-iam-ecs-role.json](https://github.com/trallnag/prometheus-ecs-discoverer/blob/master/documents/aws-iam-ecs-role.json).

### Configure Prometheus

If you want all your targets to be scraped in the same interval, the following 
job is enough.

```txt
- job_name: 'ecs'
  file_sd_configs:
    - files:
        - /tmp/tasks.json
  relabel_configs:
    - source_labels: [metrics_path]
      action: replace
      target_label: __metrics_path__
      regex: (.+)
```

By default, PromED exposes an `/metrics` endpoint.

```txt
- job_name: discovery
  static_configs: 
    - targets: ["discovery:8080"]
```

## Configuration

As this project is based on 
[prometheus-ecs-sd](https://github.com/signal-ai/prometheus-ecs-sd), 
the configuration is mostly compatible.

PromED uses [Dynconf](https://www.dynaconf.com/) for config management. There 
are two main ways you can configure the application. Either by providing a 
custom settings file with the env var `SETTINGS_FILES_FOR_DYNACONF` (see 
[here](https://www.dynaconf.com/configuration/#on-environment-options)) 
or directly setting the respective values via env vars with the `DYNACONF_` 
prefix. All supported settings together with their default values can be found 
[`settings.toml` (click me)](https://github.com/trallnag/prometheus-ecs-discoverer/blob/master/prometheus_ecs_discoverer/settings.toml).

## Grafana Dashboard

You can find the Grafana dashboards for PromED in the documents folder 
and in the Grafana cloud.

![dashboard-screenshot](https://raw.githubusercontent.com/trallnag/prometheus-ecs-discoverer/master/documents/screenshot-dashboard-PromED-HighR.png)

There are two dashboards available. One always draws data with the highest 
possible resolution (PromED HighR). This dashboard is recommended for close-up
interactions on a narrow time range. PromED LowR draws data with a larger 
resolution that tends to average out more. Can be used for wide time ranges 
and trend discovery. 

A third dashboard contains panels with Grafana Alerts enabled.

![dashboard-screenshot](https://raw.githubusercontent.com/trallnag/prometheus-ecs-discoverer/master/documents/screenshot-dashboard-PromED-Alerting.png)

## Prerequesites

See [pyproject.toml](https://github.com/trallnag/prometheus-ecs-discoverer/blob/master/pyproject.toml).

## Development

Developing and building this package on a local machine requires 
[Python Poetry](https://python-poetry.org/). I recommend to run Poetry in 
tandem with [Pyenv](https://github.com/pyenv/pyenv). Once the repository is 
cloned, run `poetry install` and `poetry shell`. From here you may start the 
IDE of your choice.

**WORK IN PROGRESS, RELEASE BEGINNING OF AUGUST**

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
Prometheus by setting environment variables in the task's definition.

What are the advantages of using this project over [prometheus-ecs-sd](https://github.com/signal-ai/prometheus-ecs-sd
)?

* Modified throttling allows the usage in environments with hundreds of 
    tasks.
* Every target can expose custom labels via its environment variables.
* Deploy as container (provided and can be used directly) or Python package.
* Instrumented with Prometheus. Allows more insights into the discoverer.
* Extensive testing with high coverage ensures functionality.
* Works out of the box with being deployed in a container.
* More configuration options.

Contents: **[Setup](#setup)** | **[Configuration](#configuration)** |

## Setup

As this project is based on 
[prometheus-ecs-sd](https://github.com/signal-ai/prometheus-ecs-sd), the setup 
is very similar / exactly the same.

1. Prepare targets
2. Deploy PromED
3. Configure Prometheus

### **Prepare targets**

Targets are setup via setting environment variables in the task definitions.

#### Mark container as target

Set `PROMETHEUS` to any value to make PromED consider the container. This 
by itself is already enough to make it work with the configured defaults.

```json
{ "name": "PROMETHEUS", "value": "does not matter" },
```

#### Specify metrics endpoint(s)

If your metrics are not exposed on the default `/metrics` endpoint, you can 
specifiy the endpoint like so:

```json
{ "name": "PROMETHEUS_ENDPOINT", "value": "/custom/metrics" },
```

You can also declare multiple endpoints and different intervals. The supported 
intervals are `15s`, `30s`, `1m` and `5m`. Based on the interval targets will 
end up in different files. The default interval is "generic". Examples for this:

```json
{ "name": "PROMETHEUS_ENDPOINT", "value": "5m:/mymetrics,30s:/mymetrics2"},
{ "name": "PROMETHEUS_ENDPOINT", "value": "/mymetrics"},
{ "name": "PROMETHEUS_ENDPOINT", "value": "/mymetrics,30s:/mymetrics2"},
```

#### Set custom labels for container

Sometimes you might want to add additonal labels to targets to group them. 
For example by the used API type (REST vs. GraphQL). This can be done by adding 
environment variables to the container definition in the respective task 
definition with the  `PROMETHEUS_LABEL_` prefix. Environment variables set
from within the container are not visible to PromED and are ignored.

```json
{ "name": "PROMETHEUS_LABEL_api_type", "value": "GraphQL" },
{ "name": "PROMETHEUS_LABEL_foo", "value": "bar" },
``` 

#### Customize networking

Regarding networking, all network modes are supported (`bridge`, `host` 
and `awsvpc`).

> If `PROMETHEUS_PORT` and `PROMETHEUS_CONTAINER_PORT` are not set, the script 
> will pick the first port from the container definition (in awsvpc and host 
> network mode) or the container host network bindings in bridge mode. On 
> Fargate, if `PROMETHEUS_PORT` is not set, it will default to port `80`.
> 
> If `PROMETHEUS_CONTAINER_PORT` is set, it will look at the container host 
> network bindings, and find the entry with a matching `containerPort`. It will 
> then use the `hostPort` found there as target port. This is useful when the 
> container port is known, but the `hostPort` is randomly picked by ECS (by 
> setting `hostPort` to `0` in the task definition).
> 
> If your container uses multiple ports, it's recommended to specify 
> `PROMETHEUS_PORT` (`awsvpc`, `host`) or `PROMETHEUS_CONTAINER_PORT` (`bridge`).

Quoted from [prometheus-ecs-sd](https://github.com/signal-ai/prometheus-ecs-sd) 
commit `ece6ca2`.

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
[`settings.toml` (click me)](prometheus_ecs_discoverer/settings.toml).

Here are a few notable settings (together with their defaults) you can modify:

```sh
INTERVAL = 15
OUTPUT_DIRECTORY = "/tmp"

# Throttles the first discovery run to ensure that even hundreds of tasks and 
# definitions don't overwhelm the AWS API while building up the local cache.
WARMUP_THROTTLE = true
THROTTLE_INTERVAL_SECONDS = 0.1

# Exposes metrics about discoverer itself.
PROMETHEUS_START_HTTP_SERVER = true
PROMETHEUS_SERVER_PORT = 8080

# If no endpoint is given in the respective env var, this will be used.
FALLBACK_METRICS_ENDPOINT = "/metrics"

# And more. See `settings.toml` file.
```

For example if you want to override fallback metrics endpoint you can either 
provide your own settings file or just do:

```sh 
export DYNACONF_FALLBACK_METRICS_ENDPOINT=/custom/metrics
``` 


<!-- ### Add custom labels to an ECS task



-->
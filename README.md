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

What are the advantages of using this project over [prometheus-ecs-sd](https://github.com/signal-ai/prometheus-ecs-sd
)?

* Modified throttling allows the usage in environments with hundreds of 
    tasks.
* Custom labels can be exposed to Prometheus by adding them to the container 
    definition.
* Deployment via a container (provided and can be used directly) or Python package.
* Extensive testing with high coverage ensures functionality.
* More configuration options.

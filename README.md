# Prometheus ECS Discoverer

Prometheus service discovery for AWS ECS leveraging the AWS API.

This projects allows your Prometheus to discover services running in ECS without relying on proper service discovery with tools like Route53 or Consul.
It can be deployed as a single container or service. The Prometheus ECS Discoverer works by querying the AWS API and updating a JSON file that can 
be used by Prometheus with its file service discovery feature.

Based on https://github.com/signal-ai/prometheus-ecs-sd. Changes and additions include:

* Environment variables set in the container definition can be propagated as additional labels to Prometheus.
* Improved project structure and overall refactoring of the code.
* Tests with high coverage. No tests at all in the project this is based on.
* Python package in PyPI and a Docker image.

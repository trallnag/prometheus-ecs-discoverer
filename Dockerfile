FROM bitnami/python:3.8-prod

LABEL MAINTAINER="tim.schwenke+trallnag@protonmail.ch"

ARG PYPI_VERSION

RUN pip install "prometheus_ecs_discoverer==${PYPI_VERSION}"

CMD [ "python", "-m", "prometheus_ecs_discoverer.run" ]

FROM bitnami/python:3.8-prod

LABEL MAINTAINER="tim.schwenke+trallnag@protonmail.ch"

RUN pip install prometheus_ecs_discoverer

CMD [ "python", "-m", "prometheus_ecs_discoverer.run" ]

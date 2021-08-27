FROM bitnami/python:3.9-prod

ENV POETRY_VERSION=1.1.8

WORKDIR /app

RUN pip install poetry==$POETRY_VERSION

COPY poetry.lock pyproject.toml .

RUN poetry install --no-root --no-dev --no-ansi

COPY prometheus_ecs_discoverer .

RUN poetry install --no-dev --no-ansi

CMD ["poetry", "run", "python", "-m", "prometheus_ecs_discoverer.main"]

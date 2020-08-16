.PHONY: all
all: lint format_style format_imports test docs requirements

.PHONY: lint
lint:
	poetry run flake8 --config .flake8 --statistics

.PHONY: format_style
format_style:
	poetry run black .

.PHONY: format_imports
format_imports:
	poetry run isort --profile black .

.PHONY: test
test:
	poetry run pytest --cov=./ --cov-report=xml

.PHONY: docs
docs:
	rm -rf docs/*; \
	mkdir -p docs; \
	poetry run pdoc --output-dir /tmp/pfi_docs --html prometheus_fastapi_instrumentator; \
	mv /tmp/pfi_docs/prometheus_fastapi_instrumentator/* docs/; 

.PHONY: requirements
requirements:
	poetry run pip freeze > requirements.txt

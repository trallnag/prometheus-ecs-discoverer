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
	rm -rf pdoc3/*; \
	mkdir -p pdoc3; \
	poetry run pdoc --output-dir /tmp/pdoc3 --html prometheus_ecs_discoverer; \
	mv /tmp/pdoc3/prometheus_ecs_discoverer/* pdoc3/; 

.PHONY: requirements
requirements:
	poetry run pip freeze > requirements.txt

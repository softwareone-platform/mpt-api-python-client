.PHONY: bash build check check-all down format review test help

DC = docker compose -f compose.yaml

help:
	@echo "Available commands:"
	@echo "  make bash             - Open a bash shell in the app container."
	@echo "  make build            - Build images."
	@echo "  make check            - Check code quality with ruff."
	@echo "  make check-all        - Run check and tests."
	@echo "  make down             - Stop and remove containers."
	@echo "  make e2e              - Run e2e test."
	@echo "  make format           - Format code."
	@echo "  make review           - Check the code in the cli by running CodeRabbit."
	@echo "  make test             - Run tests."
	@echo "  make help             - Display this help message."

bash:
	  $(DC) run --rm -it app bash

build:
	  $(DC) build

check:
	  $(DC) run --rm app bash -c "ruff format --check . && ruff check . && flake8 . && mypy . && uv lock --check"

check-all:
	  make check
	  make test

down:
	  $(DC) down

format:
	  $(DC) run --rm app bash -c "ruff check --select I --fix . && ruff format ."

review:
	  coderabbit review --prompt-only

test:
	  $(DC) run --rm app pytest $(args) tests/unit

test-all:
	  make test
	  make e2e

e2e:
	  $(DC) run --rm app pytest -p no:randomly --junitxml=e2e-report.xml $(args) tests/e2e

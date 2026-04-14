# Contributing

This document captures repository-specific contribution guidance. Shared engineering rules
live in `mpt-extension-skills` and should be linked, not copied, from this repository.

## Shared Standards

- [Python coding conventions](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/standards/python-coding.md)
- [Packages and dependencies](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/standards/packages-and-dependencies.md)
- [Pull requests](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/standards/pull-requests.md)
- [Repository documentation](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/standards/documentation.md)
- [Makefile structure](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/standards/makefiles.md)

## Shared Knowledge

- [Build and checks](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/knowledge/build-and-checks.md)
- [Make target meanings](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/knowledge/make-targets.md)

## Development Model

This repository uses Docker as the default local execution model.

- Use `make build` to build the container image.
- Use `make bash` when you need an interactive shell inside the container.
- Use `make run` for an IPython session with project dependencies available.
- Use `make test`, `make check`, and `make check-all` through the provided `make` targets.

## Repository-Specific Expectations

- Keep public API changes aligned with [`mpt_api_client/mpt_client.py`](../mpt_api_client/mpt_client.py) and the resource/service layout described in [architecture.md](architecture.md).
- Keep resource-specific behavior inside the matching module under [`mpt_api_client/resources/`](../mpt_api_client/resources).
- Keep transport and query behavior inside [`mpt_api_client/http/`](../mpt_api_client/http) and [`mpt_api_client/rql/`](../mpt_api_client/rql).
- Add or update tests near the affected domain under [`tests/unit/`](../tests/unit) or [`tests/e2e/`](../tests/e2e).
- When repository behavior changes, update the narrowest relevant document under [`docs/`](.).

## Validation Before Review

Follow the shared validation flow from
[knowledge/build-and-checks.md](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/knowledge/build-and-checks.md).

In this repository, run validation through the Docker-based targets documented in
[testing.md](testing.md). Use `make build` first when dependencies or `uv.lock` change.

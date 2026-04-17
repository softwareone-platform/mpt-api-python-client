# AGENTS.md

This file is the AI assistant entry point for `mpt-api-python-client`.

## Working Protocol

For any task in this repository:

1. Identify the task type and select only the local repository files that are relevant to that task.
2. Read only those relevant local files before making changes.
3. If any selected local file references shared standards or shared operational guidance that are relevant to the same task, read those shared documents too before proceeding.
4. Treat repository-local documents as repository-specific additions, restrictions, or overrides to shared guidance.
5. If a repository-local rule conflicts with a shared rule, the local repository rule takes precedence.

## Repository Purpose

Python API client for the SoftwareONE Marketplace Platform (MPT) API. Provides synchronous
(`MPTClient`) and asynchronous (`AsyncMPTClient`) clients built on httpx, with typed
resource services, mixin-based HTTP operations, and an RQL query builder.

## Documentation Reading Order

When applicable, read the repository documentation in this order:

1. `README.md` — project overview and quick start
2. `docs/architecture.md` — layered architecture, directory structure, key abstractions
3. `docs/testing.md` — test structure, tooling, conventions, how to run tests
4. `docs/contributing.md` — development workflow, coding conventions, linting setup
5. `docs/local-development.md` — Docker setup, Make targets, environment variables

## Library Usage

See `docs/PROJECT_DESCRIPTION.md` for installation and usage examples (sync and async).

## API Reference

The upstream MPT API is described by the OpenAPI spec:
https://api.s1.show/public/v1/openapi.json

Use this to understand available endpoints, request/response schemas, and field names.

## Key Commands

| Command          | Purpose                                  |
|------------------|------------------------------------------|
| `make build`     | Build the Docker development environment |
| `make test`      | Run unit tests                           |
| `make check`     | Run all linting and type checks          |
| `make check-all` | Run checks + tests                       |
| `make format`    | Auto-format code                         |

## Project Structure

```text
mpt_api_client/
├── mpt_client.py       # MPTClient / AsyncMPTClient entry points
├── http/               # HTTP transport, services, mixins
├── resources/          # API domain modules (catalog, commerce, billing, …)
├── models/             # Response model classes
├── rql/                # RQL query builder
└── exceptions.py       # Error hierarchy
```

## Shared Standards

This repository follows shared engineering standards from
[mpt-extension-skills](https://github.com/softwareone-platform/mpt-extension-skills):

- `standards/python-style-guide.md`
- `standards/testing-standard.md`
- `standards/contributing-standard.md`
- `standards/pull-request-guidelines.md`


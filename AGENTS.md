# AGENTS.md

Working protocol for any task in this repository:

1. Identify the task type and select only the local repository files that are relevant to that task.
2. Read only those relevant local files before making changes.
3. If any selected local file references shared standards or shared operational guidance that are relevant to the same task, read those shared documents too before proceeding.
4. Treat repository-local documents as repository-specific additions, restrictions, or overrides to shared guidance.
5. If a repository-local rule conflicts with a shared rule, the local repository rule takes precedence.

Python API client for the SoftwareONE Marketplace Platform (MPT) API. Provides synchronous
(`MPTClient`) and asynchronous (`AsyncMPTClient`) clients built on httpx, with typed
resource services, mixin-based HTTP operations, and an RQL query builder.

## Documentation Reading Order

When applicable, read the repository documentation in this order:

1. `README.md` — repository overview, quick start, and documentation map
2. `docs/usage.md` — installation, configuration, Python usage examples, and supported Docker-based commands
3. `docs/architecture.md` — layered architecture, directory structure, and key abstractions
4. `docs/local-development.md` — Docker-only setup and execution model
5. `docs/testing.md` — repository-specific testing strategy and command mapping
6. `docs/contributing.md` — repository-specific workflow and links to shared standards
7. `docs/documentation.md` — repository-specific documentation rules

Then inspect the code paths relevant to the task:

- `mpt_api_client/mpt_client.py` — public sync and async client entry points
- `mpt_api_client/http/` — HTTP clients, services, query state, and reusable mixins
- `mpt_api_client/resources/` — domain resource groups such as catalog, commerce, billing, and integration
- `mpt_api_client/models/` — response model layer and collection wrappers
- `mpt_api_client/rql/` — fluent RQL query builder
- `tests/unit/` — unit coverage for transport, resources, models, and query builder
- `tests/e2e/` — live API coverage by domain
- `make/` and `compose.yaml` — Docker-based local command entry points

## API Reference

The upstream API contract is the MPT OpenAPI spec:
https://api.s1.show/public/v1/openapi.json

## Key Commands

| Command          | Purpose                                  |
|------------------|------------------------------------------|
| `make build`     | Build the Docker development environment |
| `make test`      | Run unit tests                           |
| `make check`     | Run all linting and type checks          |
| `make check-all` | Run checks + tests                       |
| `make format`    | Auto-format code                         |
| `make bash`      | Open a shell in the Docker container     |
| `make run`       | Start an IPython session in Docker       |

## Repository Rules

- Prefer Docker-based `make` targets over ad hoc local Python commands.
- Keep `README.md` concise and navigational.
- Put topic-specific documentation under `docs/` instead of expanding `README.md`.
- Link shared engineering rules from `mpt-extension-skills` instead of duplicating them locally.

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

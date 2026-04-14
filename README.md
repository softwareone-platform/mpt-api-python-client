# mpt-api-python-client

Python API client for the SoftwareONE Marketplace Platform (MPT) API.

Provides synchronous (`MPTClient`) and asynchronous (`AsyncMPTClient`) clients built on
[httpx](https://www.python-httpx.org/), with typed resource services, mixin-based HTTP
operations, and an RQL query builder.

## Documentation

Start with these documents:

- [AGENTS.md](AGENTS.md): AI-agent entry point and reading order
- [docs/usage.md](docs/usage.md): installation, configuration, Python usage examples, and Docker-based commands
- [docs/architecture.md](docs/architecture.md): repository structure, layers, and key abstractions
- [docs/local-development.md](docs/local-development.md): Docker-only local setup and execution model
- [docs/testing.md](docs/testing.md): repository-specific test strategy and commands
- [docs/contributing.md](docs/contributing.md): repository-specific workflow and links to shared standards
- [docs/documentation.md](docs/documentation.md): repository-specific documentation rules
- [docs/rql.md](docs/rql.md): fluent RQL query builder guide
- [MPT OpenAPI Spec](https://api.s1.show/public/v1/openapi.json): upstream API contract

## Quick Start

```bash
cp .env.sample .env   # configure MPT_API_BASE_URL and MPT_API_TOKEN
make build
make test
```

Use `make help` to inspect all supported Docker-based commands.

See [docs/usage.md](docs/usage.md) for installation details, sync and async examples, RQL
usage, and Docker-based command examples.

## Key Commands

```bash
make build      # build Docker development environment
make test       # run unit tests
make check      # run all quality checks (ruff, flake8, mypy)
make check-all  # run checks + tests
make format     # auto-format code
make bash       # open a shell in the container
make run        # start an IPython session
```

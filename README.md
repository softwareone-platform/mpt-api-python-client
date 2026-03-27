[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=softwareone-platform_mpt-api-python-client&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=softwareone-platform_mpt-api-python-client)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=softwareone-platform_mpt-api-python-client&metric=coverage)](https://sonarcloud.io/summary/new_code?id=softwareone-platform_mpt-api-python-client)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# mpt-api-python-client

Python API client for the SoftwareONE Marketplace Platform (MPT) API.

Provides synchronous (`MPTClient`) and asynchronous (`AsyncMPTClient`) clients built on
[httpx](https://www.python-httpx.org/), with typed resource services, mixin-based HTTP
operations, and an RQL query builder.

## Quick Start

```bash
cp .env.sample .env   # configure MPT_API_BASE_URL and MPT_API_TOKEN
make build
make test
```

## Usage

**[Installation & Usage Guide](docs/PROJECT_DESCRIPTION.md)**

```python
from mpt_api_client import MPTClient

client = MPTClient()  # reads MPT_API_TOKEN and MPT_API_BASE_URL from environment

for product in client.catalog.products.iterate():
    print(product.name)
```

### RQL Filtering Example

```python
from mpt_api_client import MPTClient, RQLQuery

client = MPTClient()
products = client.catalog.products

target_ids = RQLQuery("id").in_([
    "PRD-123-456",
    "PRD-789-012",
])
active = RQLQuery(status="active")
vendor = RQLQuery("vendor.name").eq("Microsoft")

query = target_ids & active & vendor

for product in products.filter(query).order_by("-audit.updated.at").select("id", "name").iterate():
    print(product.id, product.name)
```

## Documentation

| Document                                                       | Description                                                 |
|----------------------------------------------------------------|-------------------------------------------------------------|
| [Architecture](docs/architecture.md)                           | Layered architecture, directory structure, key abstractions |
| [RQL Guide](docs/rql.md)                                       | Fluent builder for Resource Query Language filters           |
| [Contributing](docs/contributing.md)                           | Development workflow, coding conventions, linting setup     |
| [Testing](docs/testing.md)                                     | Test structure, tooling, conventions                        |
| [Local Development](docs/local-development.md)                 | Docker setup, Make targets, environment variables           |
| [Usage Guide](docs/PROJECT_DESCRIPTION.md)                     | Installation, sync and async usage examples                 |
| [MPT OpenAPI Spec](https://api.s1.show/public/v1/openapi.json) | Upstream API contract (endpoints, schemas)                  |

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

Run `make help` to see all available commands.

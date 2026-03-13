# Copilot Instructions

## Project Overview

Python client library for the SoftwareONE Marketplace (MPT) API. Provides both synchronous and asynchronous interfaces across resource domains: accounts, billing, catalog, commerce, audit, and notifications.

Requires **Python 3.12+**. All development runs inside Docker via `docker compose`.

## Commands

All commands are Docker-based and run through `make`:

```bash
make test                          # Run unit tests
make test args="tests/unit/http/test_client.py::test_http_initialization"  # Run a single test
make check                         # Lint + type-check (ruff format, ruff check, flake8, mypy, uv lock)
make format                        # Auto-format (ruff format + import sort)
make check-all                     # check + test together
make e2e                           # End-to-end tests (requires real API credentials)
make bash                          # Open shell in container
```

To run tests directly inside the container:
```bash
docker compose run --rm app pytest tests/unit/path/to/test_file.py::test_name
```

## Architecture

### Entry Points

`MPTClient` (sync) and `AsyncMPTClient` (async) in `mpt_client.py` are the public API. They expose resource groups as properties (`client.catalog.products`, `client.commerce.orders`, etc.).

### Layered Structure

```text
MPTClient / AsyncMPTClient
  └── Resource group (e.g., Catalog, Commerce)
        └── Service (e.g., ProductsService) = Service base + mixins
              └── HTTPClient / AsyncHTTPClient (wraps httpx)
```

### Resources

Each resource domain lives in `mpt_api_client/resources/<domain>/`. Every resource consists of:
- A **Model** class (e.g., `Product`) extending `Model`
- A **ServiceConfig** (e.g., `ProductsServiceConfig`) with `endpoint`, `model`, and key fields
- A **sync Service** and an **async Service** built by composing mixins

### Mixins (`mpt_api_client/http/mixins/`)

Behavior is composed via mixins. Both sync and async versions exist for each:
- CRUD: `CreateMixin`, `GetMixin`, `UpdateMixin`, `DeleteMixin`
- Collections: `CollectionMixin` (iterate, paginate, filter, order_by, select)
- Files: `CreateFileMixin`, `UpdateFileMixin`, `DownloadFileMixin`
- Domain: `PublishableMixin`, `ActivatableMixin`, `EnableMixin`, `DisableMixin`, `TerminateMixin`, `RenderMixin`, `QueryableMixin`

When adding a new service, compose only the mixins it needs. Async services mirror sync ones with `Async` prefix and `async def` methods.

### Models (`mpt_api_client/models/`)

- Inherit from `Model` (or `BaseModel`)
- Use type annotations; no explicit `__init__` needed
- **Automatic camelCase ↔ snake_case conversion** — API uses camelCase, Python uses snake_case
- Nested dicts/lists are auto-converted to model instances

### RQL Query Builder (`mpt_api_client/rql/`)

`RQLQuery` builds filter expressions for API calls. Used with `.filter()`, `.order_by()`, `.select()` on services.

## Key Conventions

### Adding a New Resource

1. Create `mpt_api_client/resources/<domain>/<resource>/` with:
   - `__init__.py` exporting the service classes
   - `models.py` — `Model` subclass
   - `services.py` — sync + async service classes (inherit `Service`/`AsyncService` + relevant mixins + `ServiceConfig`)
2. Add a property for it on the resource group class
3. Add corresponding unit tests under `tests/unit/resources/<domain>/<resource>/`

### Code Style

- Line length: **100 chars**
- Quotes: **double quotes**
- Docstrings: **Google style**
- Strict `mypy` — all public functions need type annotations
- Max McCabe complexity: **6** per function
- Ruff rules enforced: D (docstrings), FBT (no bool positional args), S (security), TRY, PLR, etc.

### Error Handling

Raise `MPTHttpError` or `MPTAPIError` (from `mpt_api_client/exceptions.py`). Use `transform_http_status_exception()` to convert httpx HTTP errors into the MPT exception hierarchy. Don't catch and swallow errors silently.

### HTTP Client Initialization

Clients can be initialized from env vars:
- `MPT_API_BASE_URL`
- `MPT_API_TOKEN`

Or explicitly:
```python
client = MPTClient.from_config(api_token="...", base_url="https://...")
```

## Test Patterns

### Mocking HTTP

Use `respx` to mock `httpx` calls:

```python
import respx
from httpx import Response


@respx.mock
def test_something(http_client):
    route = respx.get(f"{API_URL}/resource/123").mock(return_value=Response(200, json={...}))
    result = http_client.request("GET", "/resource/123")
    assert route.called
```

### Async Tests

`pytest-asyncio` is configured with `asyncio_mode = "auto"` — just write `async def test_...()`.

### Fixtures

Common fixtures are in `tests/unit/conftest.py`:
- `http_client` — `HTTPClient` instance
- `async_http_client` — `AsyncHTTPClient` instance

### Test Location

Unit tests mirror the source tree: `tests/unit/resources/catalog/products/` for `mpt_api_client/resources/catalog/products/`.

### Native Commands (no Docker)

| Task | Command |
|------|---------|
| Run all unit tests | `uv run pytest tests/unit/` |
| Run a single test | `uv run pytest tests/unit/path/to/test_file.py::test_name` |
| Run tests with coverage | `uv run pytest tests/unit/ --cov=mpt_api_client --cov-report=term-missing` |
| Format code | `uv run ruff format .` |
| Fix lint issues | `uv run ruff check . --fix` |
| Check formatting | `uv run ruff format --check .` |
| Lint | `uv run ruff check .` |
| Style check | `uv run flake8` |
| Type check | `uv run mypy mpt_api_client` |
| All quality checks | `uv run ruff format --check . && uv run ruff check . && uv run flake8 && uv run mypy mpt_api_client` |

### Verification Checklist

The agent **must** verify all of the following before submitting:

- [ ] All existing unit tests pass: `uv run pytest tests/unit/`
- [ ] New unit tests written for every new function, mixin, model, or service
- [ ] New tests follow AAA (Arrange–Act–Assert) pattern with no branching inside tests
- [ ] Code formatting is clean: `uv run ruff format --check .`
- [ ] Linting passes: `uv run ruff check . && uv run flake8`
- [ ] Type checking passes: `uv run mypy mpt_api_client`
- [ ] All public functions/methods/classes have Google-style docstrings
- [ ] No hardcoded configuration values — all config via env vars or constructor args

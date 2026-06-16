# Architecture

This document describes the internal architecture of `mpt-api-python-client`.

## Overview

`mpt-api-python-client` is a Python API client that provides a typed, fluent interface for the
SoftwareONE Marketplace Platform (MPT) REST API. It supports both synchronous and asynchronous
usage and is built on top of [httpx](https://www.python-httpx.org/).

**API Reference:** The full upstream API contract is described by the
[MPT OpenAPI Spec](https://api.s1.show/public/v1/openapi.json).
The client mirrors this spec's resource structure.

The client exposes every MPT API domain (catalog, commerce, billing, etc.) as a resource group,
where each resource is a service object composed from reusable HTTP operation mixins.

## Directory Structure

```text
mpt_api_client/
├── __init__.py              # Public API: MPTClient, AsyncMPTClient, RQLQuery
├── mpt_client.py            # Client entry points
├── constants.py             # Shared constants (content types)
├── exceptions.py            # Error hierarchy (MPTError, MPTHttpError, MPTAPIError)
│
├── http/                    # HTTP transport layer
│   ├── client.py            # Sync HTTPClient (httpx.Client)
│   ├── async_client.py      # Async AsyncHTTPClient (httpx.AsyncClient)
│   ├── base_service.py      # ServiceBase — shared service logic
│   ├── service.py           # Service — sync service (extends ServiceBase)
│   ├── async_service.py     # AsyncService — async service (extends ServiceBase)
│   ├── query_state.py       # Query parameter accumulation
│   ├── client_utils.py      # URL validation helpers
│   ├── types.py             # Type aliases (Response, HeaderTypes, etc.)
│   └── mixins/              # Composable HTTP operation mixins
│       ├── collection_mixin.py
│       ├── create_mixin.py
│       ├── create_file_mixin.py
│       ├── update_mixin.py
│       ├── update_file_mixin.py
│       ├── delete_mixin.py
│       ├── get_mixin.py
│       ├── enable_mixin.py
│       ├── disable_mixin.py
│       ├── download_file_mixin.py
│       ├── file_operations_mixin.py
│       ├── queryable_mixin.py
│       └── resource_mixins.py
│
├── models/                  # Response models
│   ├── model.py             # Model base class (camelCase ↔ snake_case mapping)
│   ├── model_collection.py  # ModelCollection — paginated result set
│   ├── meta.py              # Meta / Pagination metadata
│   └── file_model.py        # FileModel for binary responses
│
├── resources/               # API domain modules
│   ├── accounts/            # Account, Users, Buyers, Sellers, API Tokens, …
│   ├── audit/               # Audit records, Event types
│   ├── billing/             # Invoices, Ledgers, Journals, Statements, Credit memos, …
│   ├── catalog/             # Products, Listings, Price lists, Authorizations, …
│   ├── commerce/            # Agreements, Orders, Subscriptions, Assets
│   ├── exchange/            # Exchange resources
│   ├── helpdesk/            # Cases, Chats, Queues, Forms, …
│   ├── integration/         # Integration resources
│   ├── notifications/       # Messages, Batches, Subscribers, …
│   ├── program/             # Program resources
│   └── spotlight/           # Spotlight resources
│
└── rql/                     # RQL query builder
    ├── query_builder.py     # RQLQuery, RQLProperty, RQLValue
    └── constants.py         # RQL operator constants
```

## Layered Architecture

The client is organized into four layers:

```text
┌─────────────────────────────────────────────┐
│           MPTClient / AsyncMPTClient        │  Entry point
├─────────────────────────────────────────────┤
│         Resource Groups (domains)           │  catalog, commerce, billing, …
├─────────────────────────────────────────────┤
│   Service + Mixins (HTTP operations)        │  get, create, update, delete, iterate, …
├─────────────────────────────────────────────┤
│       HTTPClient / AsyncHTTPClient          │  httpx transport
└─────────────────────────────────────────────┘
```

### 1. Client Layer — `mpt_client.py`

`MPTClient` (sync) and `AsyncMPTClient` (async) are the public entry points.

Each client holds an HTTP client instance and exposes domain-specific resource groups as
properties:

```python
client = MPTClient.from_config(authentication=BearerTokenAuthentication("..."), base_url="...")
client.catalog  # Catalog
client.commerce  # Commerce
client.billing  # Billing
client.accounts  # Accounts
client.audit  # Audit
client.helpdesk  # Helpdesk
client.notifications  # Notifications
```

### 2. Resource Groups — `resources/`

Each resource group (e.g. `Catalog`, `Commerce`) is a plain class that groups related service
objects. For example, `Catalog` exposes `products`, `listings`, `price_lists`,
`authorizations`, `pricing_policies`, `items`, and `units_of_measure`.

Resource groups pass the HTTP client down to each service.

### 3. Service Layer — `http/service.py`, `http/async_service.py`

`Service` and `AsyncService` extend `ServiceBase` and represent a single REST resource
endpoint (e.g. `/catalog/products`).

Services are composed using **mixins** that add HTTP operations:

| Mixin | Operation |
|---|---|
| `CollectionMixin` | `iterate()` — paginated listing |
| `GetMixin` | `get(id)` — retrieve single resource |
| `CreateMixin` | `create(data)` — create resource |
| `UpdateMixin` | `update(id, data)` — update resource |
| `DeleteMixin` | `delete(id)` — delete resource |
| `CreateFileMixin` | create with file upload |
| `UpdateFileMixin` | update with file upload |
| `DownloadFileMixin` | download binary content |
| `EnableMixin` / `DisableMixin` | enable/disable actions |
| `QueryableMixin` | `filter()`, `order_by()`, `select()` — RQL query chaining |
| `StreamJSONLMixin` | `stream()` — stream JSONL records line by line (e.g. billing charges) |
| `FilesOperationsMixin` | combined file create / update / download operations |

Example service definition:

```python
class ProductsService(
    Service[Model],
    CollectionMixin,
    GetMixin,
    CreateFileMixin,
    UpdateFileMixin,
    DeleteMixin,
):
    _endpoint = "/catalog/products"
    _model_class = Model
```

### 4. HTTP Transport — `http/client.py`, `http/async_client.py`

`HTTPClient` and `AsyncHTTPClient` wrap `httpx.Client` / `httpx.AsyncClient` with:

- pluggable authentication via an `Authentication` provider (`BearerTokenAuthentication`,
  `ExtensionFrameworkAuthentication`)
- base URL resolution
- retry transport (configurable)
- error transformation into `MPTHttpError` / `MPTAPIError`
- multipart file upload support

The base URL is read from a constructor argument or the `MPT_API_BASE_URL` environment
variable; the authentication provider is always passed explicitly.

## Cross-Cutting Concerns

### RQL Query Builder — `rql/`

See [the RQL guide](rql.md) for the fluent query builder, filter chaining, and usage examples.

### Model Layer — `models/`

`Model` is a lightweight base class that:

- converts API responses from `camelCase` to `snake_case` attribute access
- supports nested model parsing
- provides `to_dict()` serialization back to `camelCase`

`Collection[Model]` wraps paginated API responses with metadata (`Meta`, `Pagination`).

### Error Handling — `exceptions.py`

All API errors are wrapped in a hierarchy:

```text
MPTError
├── MPTHttpError          # generic HTTP error (status_code, message, body)
│   └── MPTAPIError       # structured API error (payload, title, detail, trace_id)
```

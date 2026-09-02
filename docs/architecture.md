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
│   ├── json_envelope_parser.py  # Incremental {$meta, data} envelope parsing
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
│       ├── stream_jsonl_mixin.py
│       ├── streaming_mixin.py
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
| `CollectionMixin` | `iterate()` — paginated listing; inherits `StreamingMixin`, adding `stream()` |
| `GetMixin` | `get(id)` — retrieve single resource |
| `CreateMixin` | `create(data)` — create resource |
| `UpdateMixin` | `update(id, data)` — update resource |
| `DeleteMixin` | `delete(id)` — delete resource |
| `CreateFileMixin` | create with file upload |
| `UpdateFileMixin` | update with file upload |
| `DownloadFileMixin` | download binary content |
| `EnableMixin` / `DisableMixin` | enable/disable actions |
| `QueryableMixin` | `filter()`, `order_by()`, `select()` — RQL query chaining |
| `StreamingMixin` | `stream()` — streaming read mode, opted into with the `MPT-Streaming` header |
| `StreamJSONLMixin` | `stream_jsonl()` — JSONL endpoints that define their own meaning for `application/jsonl` (billing statement charges) |
| `FilesOperationsMixin` | combined file create / update / download operations |

The table lists the synchronous names; every mixin except `QueryableMixin`, which is shared,
has an `Async*` counterpart for composition with `AsyncService`.

The platform streaming contract (`StreamingMixin` / `AsyncStreamingMixin`) exposes
`stream()`, while the endpoint-specific JSONL contract (`StreamJSONLMixin` /
`AsyncStreamJSONLMixin`) exposes `stream_jsonl()`, so a service can expose both without
the method names colliding. `CollectionMixin` and `AsyncCollectionMixin` inherit the
platform streaming mixins, so every collection service carries `stream()` without
composing them explicitly; do not list `StreamingMixin` before a collection service's
`CollectionMixin` base, because that ordering cannot produce a consistent MRO. The platform mixins request the
streaming read mode on a regular collection route and require the API to echo the
`MPT-Streaming` response header, raising `MPTStreamingNotEnabledError` when it does not. They
also verify completeness: the declared `MPT-Item-Count` is read before the first record —
raising `MPTStreamingItemCountMissingError` when absent or unusable — and compared with the
count of raw records consumed once the body is fully consumed, raising
`MPTStreamingIncompleteError` on mismatch. The count is taken before `skip_deleted` withholds
any stub, so a filtered stub still counts. An iterator closed early skips the comparison. A record marked with
`$meta.deleted` is a deletion stub rather than data, and is yielded as a `DeletionStub`
instead of a model, so it still counts towards the declared item count but cannot be ingested
as a record. A consumer that ingests no deletions can opt out with the keyword-only
`skip_deleted=True`, which withholds stubs at yield time — after the completeness bookkeeping
and the progress tick — and is typed with overloads, so the call narrows to an iterator of
models. The JSONL mixins serve endpoints that assign `application/jsonl` their own
meaning outside streaming mode.

`stream()` picks its wire format per request with the `stream_format` argument, which sets
`Accept`: `StreamFormat.JSONL` (the default) reads one record object per line, and
`StreamFormat.JSON` reads the standard `{$meta, data}` envelope. Both formats are parsed as the
body arrives and yield the same objects through the same record path, so deletion stubs, the
completeness check and the streaming error types are format-independent, and a body the client
cannot parse raises `json.JSONDecodeError` in either format. The one asymmetry is a body cut
short mid-record: the line-delimited reader hits it as a malformed last line and raises the
decode error, while the envelope reader loses the record and reports the more precise
`MPTStreamingIncompleteError`. The envelope is tokenized by
`JSONEnvelopeParser` (`http/json_envelope_parser.py`), which emits a record when its closing
brace arrives rather than when the body completes, consumes the insignificant whitespace a
streaming response emits between tokens as keep-alives, and surfaces `$meta.pagination.total`
as a parse event that `stream()` deliberately does not forward to a `progress` receiver —
the receiver's total comes from the `MPT-Item-Count` header; see
[the streaming guide](streaming.md#reporting-progress) for the consumer-facing progress
contract. The parser reads the record array out of the service's `_collection_key`, the
member the paged path deserializes, so streamed and paged responses read the same envelope.

`StreamingMixin.stream()` takes `limit` and `offset` and forwards them to the collection route
unchanged, omitting whichever is unset. Validating them locally is deliberately out of scope:
the server owns pagination-input validation, and the inputs it accepts in streaming mode are
still changing.

See [the streaming guide](streaming.md) for the consumer-facing contract these mixins
implement.

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
  `EnvTokenAuthentication`)
- base URL resolution
- retry transport (configurable)
- error transformation into `MPTHttpError` / `MPTAPIError`
- multipart file upload support

Transport-level settings (`base_url`, `timeout`, `retries`) are grouped in the
`TransportSettings` dataclass (`http/transport_settings.py`), passed to the client
constructors as `transport=TransportSettings(...)`. Timeouts resolve per connection phase:
`connect_timeout`, `read_timeout`, `write_timeout` and `pool_timeout` each fall back to
`timeout`, and the dataclass exposes two profiles — `request_timeout` for regular requests and
`stream_timeout`, whose read phase is the larger of `stream_read_timeout` and `read_timeout`,
because a streamed response defers its first byte until the server has built the result set. To resolve the base URL from the
`MPT_API_BASE_URL` environment variable instead, pass `EnvTransportSettings()` (the
default when no transport is given); the clients themselves never read the environment.
The resolved settings are handed to the authentication provider through
`Authentication.configure(transport)` at client construction time. The authentication
provider is always passed explicitly.

## Cross-Cutting Concerns

### RQL Query Builder — `rql/`

See [the RQL guide](rql.md) for the fluent query builder, filter chaining, and usage examples.

### Model Layer — `models/`

`Model` is a lightweight base class that:

- converts API responses from `camelCase` to `snake_case` attribute access
- supports nested model parsing
- provides `to_dict()` serialization back to `camelCase`

`Collection[Model]` wraps paginated API responses with metadata (`Meta`, `Pagination`).

`DeletionStub` (`models/deletion_stub.py`) is deliberately not a `Model`. It carries only the
`id` of a row deleted after a stream's membership snapshot, which is the only property the
platform guarantees on a `$meta.deleted` stub, so the type keeps a stub from being mistaken
for a record with unset fields. It is distinct from the domain `DELETED` status, which is a
state of a full record.

### Error Handling — `exceptions.py`

Client, transport, and API errors use the following hierarchy:

```text
MPTError
├── MPTStreamingError                       # base for streaming-mode failures
│   ├── MPTStreamingNotEnabledError         # response did not confirm streaming mode
│   ├── MPTStreamingFormatMismatchError     # Content-Type differed from the requested format
│   ├── MPTStreamingItemCountMissingError   # no usable MPT-Item-Count declared
│   ├── MPTStreamingIncompleteError         # record count differed from MPT-Item-Count
│   └── MPTStreamingTruncatedError          # body ended before the HTTP message completed
├── MPTMaxRetryError                        # retry attempts exhausted
└── MPTHttpError                            # generic HTTP error (status_code, message, body)
    ├── MPTAPIError                         # structured API error (payload, title, detail, trace_id)
    ├── MPTStreamingNotSupportedError       # 501, resource cannot stream (also MPTStreamingError)
    ├── MPTStreamingNotAcceptableError      # 406, format unsupported (also MPTStreamingError)
    └── MPTStreamingOverCapError            # 413, export over cap (also MPTStreamingError)
```

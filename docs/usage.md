# Usage

This guide is for developers who need to install the library, configure the client, and use
its sync or async APIs in their own code.

## Installation

Install the package with `pip` or `uv`:

```bash
pip install mpt-api-client
uv add mpt-api-client
```

## Prerequisites

- Python 3.12+
- Access to an MPT API base URL
- An MPT API token

## Configuration

The client requires a base URL and an authentication provider.

Environment variables:

| Variable           | Required | Description                        |
|--------------------|----------|------------------------------------|
| `MPT_API_BASE_URL` | yes      | SoftwareONE Marketplace API URL    |

The base URL can be read from the environment; the authentication provider is always passed
explicitly.

Example `.env` snippet:

```env
MPT_API_BASE_URL=<YOUR_MPT_API_BASE_URL>
```

## Authentication

Authentication is provided through an `Authentication` provider passed to the client. Two
implementations are available:

- `BearerTokenAuthentication` — a single, long-lived token passed explicitly.
- `EnvTokenAuthentication` — a long-lived token read from an environment variable
  (default `MPT_API_TOKEN`, configurable via the `env_var` argument).

## Instantiate The Client

With a long-lived bearer token:

```python
from mpt_api_client import MPTClient, BearerTokenAuthentication

client = MPTClient.from_config(
    authentication=BearerTokenAuthentication("<token>"),
    base_url="https://api.s1.show/public",
)
```

With the token read from the environment (`MPT_API_TOKEN`):

```python
from mpt_api_client import MPTClient, EnvTokenAuthentication

client = MPTClient.from_config(
    authentication=EnvTokenAuthentication(),
    base_url="https://api.s1.show/public",
)
```

`from_config` also accepts a `timeout` argument (HTTP request timeout in seconds, default `60.0`).

### Timeouts

`timeout` sets every connection phase at once. To tune them separately, pass a
`TransportSettings` instance and set only the phases you care about; each unset phase falls
back to `timeout`:

```python
from mpt_api_client import BearerTokenAuthentication, MPTClient, TransportSettings
from mpt_api_client.http import HTTPClient

client = MPTClient(
    http_client=HTTPClient(
        transport=TransportSettings(
            base_url="https://api.s1.show/public",
            timeout=20.0,
            connect_timeout=5.0,
            read_timeout=60.0,
        ),
        authentication=BearerTokenAuthentication("<token>"),
    )
)
```

Two things are worth knowing:

- The **read** timeout, not the connect timeout, governs how long the client waits for a
  response to start arriving. A server that accepts the connection and then thinks before
  replying is bounded by `read_timeout`.
- Streaming requests use `stream_read_timeout` (default `120.0`) in place of the regular read
  timeout, because a streamed response commits its status only after the server has built the
  result set — so the first byte can be deferred far longer than for a regular call. The
  effective streaming read timeout is never lower than `read_timeout`, so raising that raises
  both.

No total-duration timeout is applied. A long export runs for as long as the server keeps
sending; the limits are per phase, not overall.

## Synchronous Usage Patterns

Read a single resource:

```python
from mpt_api_client import MPTClient, BearerTokenAuthentication

client = MPTClient.from_config(
    authentication=BearerTokenAuthentication("<token>"),
    base_url="https://api.s1.show/public",
)

product = client.catalog.products.get("PRD-123-456")
print(product.name)
```

Iterate through a collection:

```python
from mpt_api_client import MPTClient, BearerTokenAuthentication

client = MPTClient.from_config(
    authentication=BearerTokenAuthentication("<token>"),
    base_url="https://api.s1.show/public",
)

for invoice in client.billing.invoices.iterate():
    print(invoice.id)
```

Report progress while iterating by passing an object that implements the `Progress`
protocol (`mpt_api_client.models.Progress`). `set_total_items` is called after each
page fetch, `item_processed` once per record, and `completed` when iteration finishes.
The client ships `ConsoleProgress`, which prints `Fetched X of Y - P%` to stderr
at most once per configurable interval:

```python
import datetime as dt

from mpt_api_client.models import ConsoleProgress

progress = ConsoleProgress(interval=dt.timedelta(seconds=5))
for invoice in client.billing.invoices.iterate(batch_size=50, progress=progress):
    print(invoice.id)
```

Any object implementing the three protocol methods works the same way. For custom
renderers, extend one of the abstract `ProgressReport` bases instead of implementing
the protocol from scratch: `TimeProgressReport` reports at most once per time interval
and `BatchProgressReport` once every `batch_size` records. Both track the count and
total for you — implement only `report(current, total, *, completed)`:

```python
from mpt_api_client.models import BatchProgressReport


class LogProgress(BatchProgressReport):
    def report(self, current, total, *, completed):
        logger.info("Processed %s of %s records", current, total)


for invoice in client.billing.invoices.iterate(progress=LogProgress(batch_size=1000)):
    print(invoice.id)
```

`report` is called with `completed=True` exactly once, when iteration finishes.

> **Note:** when a response carries no pagination total (missing `$meta`),
> `set_total_items` is still called but receives `0` — treat a total of `0` as
> unknown when rendering progress.

The `progress` parameter is also accepted by both `stream()` variants described in
[Streaming Large Result Sets](#streaming-large-result-sets); there `set_total_items` is never
called because a streamed response carries no pagination total, so design progress
implementations for an unknown total. The async `iterate()` and `stream()` accept an
`AsyncProgress` implementation whose methods are `async def` and are awaited —
`AsyncConsoleProgress` is the shipped counterpart, with `AsyncProgressReport`,
`AsyncTimeProgressReport`, and `AsyncBatchProgressReport` as the async abstract bases.

## Asynchronous Usage Patterns

```python
import asyncio

from mpt_api_client import AsyncMPTClient, BearerTokenAuthentication


async def main():
    client = AsyncMPTClient.from_config(
        authentication=BearerTokenAuthentication("<token>"),
        base_url="https://api.s1.show/public",
    )

    product = await client.catalog.products.get("PRD-123-456")
    print(product.name)

    async for item in client.catalog.products.iterate():
        print(item.id, item.name)


asyncio.run(main())
```

## Streaming Large Result Sets

The platform can return a full filtered result set as a single stream instead of a paged
collection. Streaming is opted into per request with the `MPT-Streaming` header, which
`StreamingMixin` and `AsyncStreamingMixin` send on your behalf. Records are yielded one at a
time without buffering the whole body, so memory stays flat regardless of result size.

No shipped service composes these mixins yet, so compose a service to reach streaming:

```python
from mpt_api_client import MPTClient, BearerTokenAuthentication, RQLQuery
from mpt_api_client.http import Service
from mpt_api_client.http.mixins import StreamingMixin
from mpt_api_client.models import Model


class OrdersStreamService(StreamingMixin[Model], Service[Model]):
    _endpoint = "/public/v1/commerce/orders"
    _model_class = Model


client = MPTClient.from_config(
    authentication=BearerTokenAuthentication("your-token"),
    base_url="https://api.example.com",
)
service = OrdersStreamService(http_client=client.http_client)

for order in service.filter(RQLQuery(status="Processing")).stream():
    print(order.id)
```

Streaming mixins extend `QueryableMixin`, so `filter()`, `order_by()` and `select()` chain
before `stream()` exactly as they do before `iterate()`. Membership is fixed when the stream
opens: records created afterwards are not included.

### Bounding An Export

By default `stream()` sends no `limit`, which exports the full snapshot; passing `limit=-1`
requests the same thing explicitly. An explicit `limit=N` bounds the export to the first `N`
records of the stream order, for a "first 100K by this sort" read that does not page:

```python
for order in service.order_by("-audit.created.at").stream(limit=100_000):
    print(order.id)
```

Under a bounded limit the counts the response reports — the `MPT-Item-Count` header and
`$meta.pagination.total` — describe the stream itself, `min(matches, N)`, not the uncapped
number of matches.

`stream()` also accepts `offset`. Pagination inputs are sent exactly as given and are never
checked locally, because the server owns their validation: it currently rejects `offset` in
streaming mode with `400`, and support for it is scheduled. Passing through is correct either
way, so no client release is coupled to that change.

The async form yields from an async generator:

```python
import asyncio

from mpt_api_client import AsyncMPTClient, BearerTokenAuthentication
from mpt_api_client.http import AsyncService
from mpt_api_client.http.mixins import AsyncStreamingMixin
from mpt_api_client.models import Model


class AsyncOrdersStreamService(AsyncStreamingMixin[Model], AsyncService[Model]):
    _endpoint = "/public/v1/commerce/orders"
    _model_class = Model


async def main():
    client = AsyncMPTClient.from_config(
        authentication=BearerTokenAuthentication("<token>"),
        base_url="https://api.s1.show/public",
    )
    service = AsyncOrdersStreamService(http_client=client.http_client)

    async for order in service.stream():
        print(order.id)


asyncio.run(main())
```

### Streaming Errors

All streaming-specific failures derive from `MPTStreamingError`, so one handler covers them:

| Exception | Raised when |
|---|---|
| `MPTStreamingNotEnabledError` | The response does not echo `MPT-Streaming`, so the body is an ordinary paged response |
| `MPTStreamingNotSupportedError` | `501` — the resource provides no streaming-capable execution strategy |
| `MPTStreamingNotAcceptableError` | `406` — the requested format cannot be served for this read mode |
| `MPTStreamingOverCapError` | `413` — the result set exceeds the configured `MaxExportKeys` cap |
| `MPTStreamingItemCountMissingError` | The response declares no usable `MPT-Item-Count`, so completeness cannot be verified |
| `MPTStreamingIncompleteError` | The fully consumed stream yielded a different number of records than `MPT-Item-Count` declared |
| `MPTStreamingTruncatedError` | The connection was aborted mid-body, so the response ended before the HTTP message completed |

Completeness is verified for you: streaming commits the `MPT-Item-Count` response header
with the status — the number of records the stream will carry, `min(matches, N)` under a
bounded `limit=N` — and `stream()` compares it with the number of records actually yielded
when the body ends. The header is the contract's only completeness signal and it does not
survive persisting the payload, so without this check a truncated export would end as a
silently short result.

```python
from mpt_api_client.exceptions import MPTStreamingError

try:
    for order in service.stream():
        print(order.id)
except MPTStreamingError as error:
    logger.error("Streaming unavailable: %s", error)
```

Catch the specific types when the response should differ — for example falling back to
`iterate()` on `MPTStreamingNotSupportedError`, but treating
`MPTStreamingNotAcceptableError` as a bug in the request:

```python
from mpt_api_client.exceptions import MPTStreamingNotSupportedError

try:
    records = list(service.stream())
except MPTStreamingNotSupportedError:
    records = list(service.iterate())
```

Treat the request-shape and endpoint-support failures — `MPTStreamingNotEnabledError`,
`MPTStreamingNotSupportedError`, `MPTStreamingNotAcceptableError`, `MPTStreamingOverCapError`
and `MPTStreamingItemCountMissingError` — as exactly that rather than transient failures:
retrying the same call against the same endpoint fails the same way, and an over-cap export
needs a narrower request, not a retry. `MPTStreamingIncompleteError` is different: it reports a
stream that terminated gracefully but did not match its declared count, for example after an
intermediary swallowed part of the body. Discard the partial records and re-run the export.
The three HTTP-backed types also subclass `MPTHttpError`, so existing `except MPTHttpError`
handlers keep working and `status_code` remains available. Any other HTTP status passes
through unchanged.

`MPTStreamingNotEnabledError` and `MPTStreamingItemCountMissingError` are raised before the
body is read, so no partial data is consumed. `MPTStreamingIncompleteError` can only be raised
once the body has been consumed to the end — records already yielded have been processed by
then, which is why the count must pass before the result set is treated as complete. Closing
the stream early on purpose, such as breaking out of the loop, does not raise: the check
applies only to a stream consumed to completion.

`MPTStreamingTruncatedError` is the opposite case: the API signals an internal mid-stream
failure by aborting the connection without completing the HTTP message, so it is raised after
records have already been yielded. It is not retry exhaustion — transparent retry runs while
the response is opened, and cannot re-request once the body has started, so `MPTMaxRetryError`
stays reserved for a request that never delivered a body at all.

Resume is a non-goal: a new request opens a new snapshot, so records from a failed attempt
cannot be spliced onto a later one. Discard everything the failed attempt produced and restart
the export from scratch:

```python
from mpt_api_client.exceptions import MPTStreamingTruncatedError

try:
    records = list(service.stream())
except MPTStreamingTruncatedError:
    records = list(service.stream())  # a new snapshot, not a continuation
```

### Over-Cap Exports

The API answers `413` when the result set is larger than the configured `MaxExportKeys` cap.
`MPTStreamingOverCapError` keeps the `problem+json` body as structured data on `payload`
rather than flattening it into the message, because the configured cap is the value a caller
acts on:

```python
from mpt_api_client.exceptions import MPTStreamingOverCapError

try:
    records = list(service.stream())
except MPTStreamingOverCapError as error:
    logger.error("Export refused: %s", error.payload)
    records = list(service.stream(limit=10_000))
```

`payload` is an empty mapping when the response carries no JSON body, so read it defensively.
The ways forward are the ones the body names: narrow the filter, set an explicit `limit=N`, or
split the export into key or date ranges.

> **Note:** `StreamJSONLMixin` also exposes `stream()`, but it serves endpoints that assign
> `application/jsonl` their own meaning outside streaming mode, such as billing statement
> charges. It sends no `MPT-Streaming` header and performs no confirmation check. A service
> composes one streaming mixin or the other, never both. See
> [architecture.md](architecture.md) for the distinction.

## Navigate The API Surface

The client exposes resource groups such as:

- `client.accounts`
- `client.audit`
- `client.billing`
- `client.catalog`
- `client.commerce`
- `client.exchange`
- `client.helpdesk`
- `client.integration`
- `client.notifications`
- `client.program`
- `client.spotlight`

See [architecture.md](architecture.md) for the repository structure and the
[MPT OpenAPI spec](https://docs.platform.softwareone.com/developer-resources/rest-api/openapi-specification)
for the upstream endpoint contract.

## Filtering And Querying

Use `filter()`, `order_by()`, and `select()` on queryable resources.

The full RQL syntax and builder usage are documented in [rql.md](rql.md). Treat that file as
the source of truth for query composition.

Typical example:

```python
from mpt_api_client import MPTClient, BearerTokenAuthentication, RQLQuery

client = MPTClient.from_config(
    authentication=BearerTokenAuthentication("<token>"),
    base_url="https://api.s1.show/public",
)

target_ids = RQLQuery("id").in_(["PRD-123-456", "PRD-789-012"])
active = RQLQuery(status="active")
vendor = RQLQuery("vendor.name").eq("Microsoft")

query = target_ids & active & vendor

for product in (
    client.catalog.products
    .filter(query)
    .order_by("-audit.updated.at")
    .select("id", "name")
    .iterate()
):
    print(product.id, product.name)
```

## Related Documents

- [testing.md](testing.md): validation and test command behavior
- [rql.md](rql.md): RQL builder guide
- [architecture.md](architecture.md): repository structure and abstractions
- [local-development.md](local-development.md): repository-local Docker workflow for contributors

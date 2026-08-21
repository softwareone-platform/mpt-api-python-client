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

### Streaming Confirmation

The API confirms streaming mode by echoing the `MPT-Streaming` response header. When it does
not, the body is an ordinary paged response, and consuming it as a stream would silently
return only the first page. `stream()` raises `MPTStreamingNotEnabledError` before reading the
body instead:

```python
from mpt_api_client.exceptions import MPTStreamingNotEnabledError

try:
    for order in service.stream():
        print(order.id)
except MPTStreamingNotEnabledError as error:
    logger.error("Endpoint did not stream: %s", error)
```

Treat this as a request-shape or endpoint-support problem, not a transient failure: retrying
the same call against an endpoint that does not support streaming mode fails the same way.

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

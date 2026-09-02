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
- A streaming request's read phase is bounded by the **larger** of `stream_read_timeout`
  (default `120.0`) and `read_timeout`, because a streamed response commits its status only
  after the server has built the result set — so the first byte can be deferred far longer
  than for a regular call. Raising `read_timeout` therefore raises the streaming budget too.

No total-duration timeout is applied. A long export runs for as long as the server keeps
sending; the limits are per phase, not overall.

Getting this wrong is the most commonly misdiagnosed streaming failure, because a working
export then looks like a broken one. See
[The Client-Timeout Trap](streaming.md#the-client-timeout-trap).

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
import logging

from mpt_api_client.models import BatchProgressReport

logger = logging.getLogger(__name__)


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

The `progress` parameter is also accepted by `stream()` and `stream_jsonl()` described in
[Streaming Large Result Sets](#streaming-large-result-sets). `stream()` calls
`set_total_items` with the declared `MPT-Item-Count` before the first record, in both wire
formats — see [Choosing The Wire Format](streaming.md#choosing-the-wire-format) — while
`stream_jsonl()` never calls it, so design progress
implementations to work while the total is still unknown. The async `iterate()`, `stream()`
and `stream_jsonl()` accept an
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

`CollectionMixin` inherits `StreamingMixin`, so every collection service exposes `stream()`
out of the box — no extra composition is needed:

```python
from mpt_api_client import BearerTokenAuthentication, MPTClient, RQLQuery

client = MPTClient.from_config(
    authentication=BearerTokenAuthentication("<token>"),
    base_url="https://api.s1.show/public",
)
service = client.commerce.orders

for order in service.filter(RQLQuery(status="Processing")).stream():
    print(order.id)
```

Streaming mixins extend `QueryableMixin`, so `filter()`, `order_by()` and `select()` chain
before `stream()` exactly as they do before `iterate()`. Membership is fixed when the stream
opens: records created afterwards are not included.

The minimal loop above reads `id`, which every streamed object carries; anything that touches
other fields must first branch on `DeletionStub`, as the async example does — or declare that
deletions are irrelevant with `skip_deleted=True`.

The wire format is a per-request choice — `stream_format=StreamFormat.JSONL` by default, or
`StreamFormat.JSON` for the `{$meta, data}` envelope. Both are parsed incrementally and carry
the same records; see
[Choosing The Wire Format](streaming.md#choosing-the-wire-format) for what differs.

The async form yields from an async generator:

```python
import asyncio
import uuid

from mpt_api_client import AsyncMPTClient, BearerTokenAuthentication
from mpt_api_client.models import DeletionStub


async def main():
    client = AsyncMPTClient.from_config(
        authentication=BearerTokenAuthentication("<token>"),
        base_url="https://api.s1.show/public",
    )
    service = client.commerce.orders
    attempt_id = uuid.uuid4().hex

    try:
        async for result in service.stream():
            if isinstance(result, DeletionStub):
                await stage_delete(attempt_id, result.id)
            else:
                await stage_upsert(attempt_id, result)

        # Reached only once stream() has verified the export; see the streaming guide.
        await promote(attempt_id)
    except Exception:
        # Any failure strands the staged attempt, not only MPTStreamingError.
        await discard(attempt_id)
        raise


asyncio.run(main())
```

**Read [the streaming guide](streaming.md) before shipping a stream consumer.** It covers
when to stream instead of paging, both wire formats, `limit` semantics, the streaming
exceptions, and the three obligations a consumer cannot skip — verifying completeness against
`MPT-Item-Count`, handling deletion stubs (and when
[opting out](streaming.md#opting-out-of-deletion-stubs) is legitimate), and restarting rather
than resuming a failed export — plus the timeout setting that decides whether a large export
works at all.

> **Note:** `StreamJSONLMixin` exposes the separately named `stream_jsonl()` for endpoints
> that assign `application/jsonl` their own meaning outside streaming mode, such as billing
> statement charges. It sends no `MPT-Streaming` header and performs no confirmation check.
> The distinct names let a service compose both streaming mixins side by side. See
> [the streaming guide](streaming.md#do-not-confuse-stream-with-stream_jsonl) for the
> distinction.


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
- [streaming.md](streaming.md): streaming guide — access pattern, obligations, timeouts
- [rql.md](rql.md): RQL builder guide
- [architecture.md](architecture.md): repository structure and abstractions
- [local-development.md](local-development.md): repository-local Docker workflow for contributors

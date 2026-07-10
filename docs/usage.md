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

- `BearerTokenAuthentication` — a single, long-lived token.
- `ExtensionFrameworkAuthentication` — a short-lived installation or account-scoped token
  fetched from an extension secret via `POST /installations/-/token`. It refreshes
  proactively once the token nears its JWT `exp` (default leeway 60s) and reactively on
  `401`. Request bodies are buffered in memory before sending so the `401` retry can
  replay one-shot streamed bodies intact. Pass `account_id` to request a token scoped to
  a specific account (`?account.id=<id>`); use one provider instance per account scope.

## Instantiate The Client

With a long-lived bearer token:

```python
from mpt_api_client import MPTClient, BearerTokenAuthentication

client = MPTClient.from_config(
    authentication=BearerTokenAuthentication("<token>"),
    base_url="https://api.s1.show/public",
)
```

With the extension framework (short-lived installation tokens):

```python
from mpt_api_client import MPTClient, ExtensionFrameworkAuthentication

client = MPTClient.from_config(
    authentication=ExtensionFrameworkAuthentication(secret="<extension-secret>"),
    base_url="https://api.s1.show/public",
)
```

For an account-scoped token, pass `account_id`:

```python
client = MPTClient.from_config(
    authentication=ExtensionFrameworkAuthentication(
        secret="<extension-secret>",
        account_id="<account-id>",
    ),
    base_url="https://api.s1.show/public",
)
```

`from_config` also accepts a `timeout` argument (HTTP request timeout in seconds, default `60.0`).

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

# mpt-api-python-client

mpt-api-python-client is a Python client for interacting with the MPT API

## Installation

Install with pip or your favorite PyPI package manager:

```bash
pip install mpt-api-client
```

```bash
uv add mpt-api-client
```

## Prerequisites

- Python 3.12+ in your environment

## Usage

```python
from mpt_api_client import MPTClient

# client = MPTClient(api_key=<your_api_key>, base_url=<mpt_api_url>)
client = MPTClient() # Reads MPT_API_TOKEN and MPT_API_BASE_URL from the environment

for product in client.catalog.products.iterate():
    print(product.name)
```

## Async Usage

```python
import asyncio
from mpt_api_client import AsyncMPTClient

async def main():
    # client = AsyncMPTClient(api_key=<your_api_key>, base_url=<mpt_api_url>)
    client = AsyncMPTClient() # Reads MPT_API_TOKEN and MPT_API_BASE_URL from the environment
    async for product in client.catalog.products.iterate():
        print(product.name)

asyncio.run(main())
```

## Development

For development purposes, please, check the Readme in the GitHub repository.

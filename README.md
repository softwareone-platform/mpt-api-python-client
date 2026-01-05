# mpt-api-python-client

A Python client for interacting with the MPT API.

## Installation

Install as a uv dependency:

```bash
uv add mpt-api-client
cp .env.example .env
```

## Usage

```python
from mpt_api_client import MPTClient

#client = MPTClient(api_key=os.getenv("MPT_API_KEY"), base_url=os.getenv("MPT_API_URL"))
client = MPTClient() # Will get the api_key and base_url from the environment variables

for product in client.catalog.products.iterate():
    print(product.name)
```

## Async Usage

```python
import asyncio
from mpt_api_client import AsyncMPTClient

async def main():
    # client = AsyncMPTClient(api_key=os.getenv("MPT_API_KEY"), base_url=os.getenv("MPT_API_URL"))
    client = AsyncMPTClient() # Will get the api_key and base_url from the environment variables
    async for product in client.catalog.products.iterate():
        print(product.name)

asyncio.run(main())
```

## Development

Clone the repository and install dependencies:

```bash
git clone https://github.com/albertsola/mpt-api-python-client.git
cd mpt-api-python-client
uv add -r requirements.txt
```

## Testing

Run all validations with:

```bash
make test-all
```

Run pytest with:

```bash
make test-all
```
## License

MIT

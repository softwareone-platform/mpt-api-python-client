import pytest

from mpt_api_client.exceptions import MPTAPIError
from tests.e2e.streaming.memory_probe import VOLUME_RECORDS


def _require_volume(page):
    total = page.meta.pagination.total if page.meta else 0
    if total < VOLUME_RECORDS:
        pytest.fail(
            f"Catalog items hold {total} records on this environment, fewer than the "
            f"{VOLUME_RECORDS} this coverage streams. The constant-memory assertion is "
            "only meaningful at volume, so this is a data problem, not a client failure."
        )


@pytest.fixture
def large_collection(mpt_ops):
    service = mpt_ops.catalog.items
    _require_volume(service.fetch_page(limit=1))
    return service


@pytest.fixture
async def async_large_collection(async_mpt_ops):
    service = async_mpt_ops.catalog.items
    _require_volume(await service.fetch_page(limit=1))
    return service


@pytest.fixture
def streaming_product_data():
    return {"name": "E2E Streaming Deletion Stub", "website": "https://www.example.com"}


@pytest.fixture
def deletable_product(mpt_vendor, streaming_product_data, logo_fd):
    product = mpt_vendor.catalog.products.create(streaming_product_data, file=logo_fd)

    yield product

    # The test hard-deletes the product itself, so this only cleans up a failed run.
    try:
        mpt_vendor.catalog.products.delete(product.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete product {product.id}: {error.title}")  # noqa: WPS421


@pytest.fixture
async def async_deletable_product(async_mpt_vendor, streaming_product_data, logo_fd):
    product = await async_mpt_vendor.catalog.products.create(streaming_product_data, file=logo_fd)

    yield product

    # The test hard-deletes the product itself, so this only cleans up a failed run.
    try:
        await async_mpt_vendor.catalog.products.delete(product.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete product {product.id}: {error.title}")  # noqa: WPS421

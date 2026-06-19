import pytest

from mpt_api_client.exceptions import MPTAPIError


@pytest.fixture
def product_data():
    return {"name": "Test Product", "website": "https://www.example.com"}


@pytest.fixture
def created_product(mpt_vendor, product_data, logo_fd):
    product = mpt_vendor.catalog.products.create(product_data, file=logo_fd)

    yield product

    try:
        mpt_vendor.catalog.products.delete(product.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete product {product.id}: {error.title}")  # noqa: WPS421


@pytest.fixture
async def async_created_product(async_mpt_vendor, product_data, logo_fd):
    product = await async_mpt_vendor.catalog.products.create(product_data, file=logo_fd)

    yield product

    try:
        await async_mpt_vendor.catalog.products.delete(product.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete product {product.id}: {error.title}")  # noqa: WPS421


@pytest.fixture
def parameter_group_id(e2e_config):
    return e2e_config["catalog.product.parameter_group.id"]


@pytest.fixture
def parameter_id(e2e_config):
    return e2e_config["catalog.product.parameter.id"]


@pytest.fixture
def item_group_id(e2e_config):
    return e2e_config["catalog.product.item_group.id"]

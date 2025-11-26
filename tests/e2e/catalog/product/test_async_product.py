import pytest

from mpt_api_client import RQLQuery
from mpt_api_client.exceptions import MPTAPIError


@pytest.fixture
async def async_created_product(logger, async_mpt_vendor, product_data, logo_fd):
    product = await async_mpt_vendor.catalog.products.create(product_data, icon=logo_fd)

    yield product

    try:
        await async_mpt_vendor.catalog.products.delete(product.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete product {product.id}: {error.title}")  # noqa: WPS421


@pytest.mark.flaky
def test_create_product(async_created_product, product_data):
    result = async_created_product.name == product_data["name"]

    assert result is True


@pytest.mark.flaky
async def test_update_product(async_mpt_vendor, async_created_product, logo_fd):
    update_data = {"name": "Updated Product"}

    result = await async_mpt_vendor.catalog.products.update(
        async_created_product.id,
        update_data,
        icon=logo_fd,
    )

    assert result.name == update_data["name"]


@pytest.mark.skip(reason="Leaves test products in the catalog")
@pytest.mark.flaky
async def test_product_review_and_publish(async_mpt_vendor, async_mpt_ops, async_created_product):
    await async_mpt_vendor.catalog.products.review(async_created_product.id)
    await async_mpt_ops.catalog.products.publish(async_created_product.id)


@pytest.mark.flaky
async def test_get_product(async_mpt_vendor, product_id):
    await async_mpt_vendor.catalog.products.get(product_id)  # act


@pytest.mark.flaky
async def test_product_save_settings(async_mpt_vendor, async_created_product):
    await async_mpt_vendor.catalog.products.update_settings(  # act
        async_created_product.id, {"itemSelection": True}
    )


@pytest.mark.flaky
async def test_filter_and_select_products(async_mpt_vendor, product_id):
    select_fields = ["-icon", "-revision", "-settings", "-vendor", "-statistics", "-website"]
    filtered_products = (
        async_mpt_vendor.catalog.products.filter(RQLQuery(id=product_id))
        .filter(RQLQuery(name="E2E Seeded"))
        .select(*select_fields)
    )

    result = [product async for product in filtered_products.iterate()]

    assert len(result) == 1

import pytest

from mpt_api_client import RQLQuery
from mpt_api_client.exceptions import MPTAPIError


@pytest.fixture
async def async_created_product(logger, async_mpt_vendor, product_data, product_icon):
    product = await async_mpt_vendor.catalog.products.create(product_data, icon=product_icon)

    yield product

    try:
        await async_mpt_vendor.catalog.products.delete(product.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete product {product.id}: {error.title}")  # noqa: WPS421


@pytest.mark.flaky
def test_create_product(async_created_product, product_data):
    assert async_created_product.name == product_data["name"]


@pytest.mark.flaky
async def test_update_product(async_mpt_vendor, async_created_product, product_icon):
    update_data = {"name": "Updated Product"}

    product = await async_mpt_vendor.catalog.products.update(
        async_created_product.id,
        update_data,
        icon=product_icon,
    )

    assert product.name == update_data["name"]


@pytest.mark.skip(reason="Leaves test products in the catalog")
@pytest.mark.flaky
async def test_product_review_and_publish(async_mpt_vendor, async_mpt_ops, async_created_product):
    await async_mpt_vendor.catalog.products.review(async_created_product.id)
    await async_mpt_ops.catalog.products.publish(async_created_product.id)


@pytest.mark.flaky
async def test_get_product(async_mpt_vendor, product_id, logger):
    await async_mpt_vendor.catalog.products.get(product_id)


@pytest.mark.flaky
async def test_product_save_settings(async_mpt_vendor, async_created_product):
    await async_mpt_vendor.catalog.products.update_settings(
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

    products = [product async for product in filtered_products.iterate()]
    assert len(products) == 1

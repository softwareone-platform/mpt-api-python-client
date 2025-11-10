import pytest

from mpt_api_client import RQLQuery
from mpt_api_client.exceptions import MPTAPIError


@pytest.fixture
def created_product(logger, mpt_vendor, product_data, product_icon):
    product = mpt_vendor.catalog.products.create(product_data, icon=product_icon)

    yield product

    try:
        mpt_vendor.catalog.products.delete(product.id)
    except MPTAPIError as error:
        logger.exception("TEARDOWN - Unable to delete product %s: %s", product.id, error.title)


@pytest.mark.flaky
def test_create_product(created_product, product_data):
    assert created_product.name == product_data["name"]


@pytest.mark.flaky
def test_update_product(mpt_vendor, created_product, product_icon):
    update_data = {"name": "Updated Product"}

    product = mpt_vendor.catalog.products.update(created_product.id, update_data, icon=product_icon)

    assert product.name == update_data["name"]


@pytest.mark.skip(reason="Leaves test products in the catalog")
@pytest.mark.flaky
def test_product_review_and_publish(mpt_vendor, mpt_ops, created_product):
    mpt_vendor.catalog.products.review(created_product.id)
    mpt_ops.catalog.products.publish(created_product.id)


@pytest.mark.flaky
def test_get_product(mpt_vendor, product_id):
    mpt_vendor.catalog.products.get(product_id)


@pytest.mark.flaky
def test_product_save_settings(mpt_vendor, created_product):
    mpt_vendor.catalog.products.update_settings(created_product.id, {"itemSelection": True})


@pytest.mark.flaky
def test_filter_and_select_products(mpt_vendor, product_id):
    select_fields = ["-icon", "-revision", "-settings", "-vendor", "-statistics", "-website"]

    filtered_products = (
        mpt_vendor.catalog.products.filter(RQLQuery(id=product_id))
        .filter(RQLQuery(name="E2E Seeded"))
        .select(*select_fields)
    )

    products = list(filtered_products.iterate())
    assert len(products) == 1

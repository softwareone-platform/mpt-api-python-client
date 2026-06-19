import pytest

from mpt_api_client import RQLQuery

pytestmark = [pytest.mark.flaky]


def test_create_product(created_product, product_data):
    result = created_product.name == product_data["name"]

    assert result is True


def test_update_product(mpt_vendor, created_product, logo_fd):
    update_data = {"name": "Updated Product"}

    result = mpt_vendor.catalog.products.update(created_product.id, update_data, file=logo_fd)

    assert result.name == update_data["name"]


def test_product_review_and_publish(mpt_vendor, mpt_ops, created_product):
    mpt_vendor.catalog.products.review(created_product.id)

    mpt_ops.catalog.products.publish(created_product.id)  # act


def test_get_product(mpt_vendor, product_id):
    mpt_vendor.catalog.products.get(product_id)  # act


def test_product_save_settings(mpt_vendor, created_product):
    mpt_vendor.catalog.products.update_settings(created_product.id, {"itemSelection": True})  # act


def test_filter_and_select_products(mpt_vendor, product_id):
    select_fields = ["-icon", "-revision", "-settings", "-vendor", "-statistics", "-website"]
    filtered_products = (
        mpt_vendor.catalog.products
        .filter(RQLQuery(id=product_id))
        .filter(RQLQuery(name="E2E Seeded"))
        .select(*select_fields)
    )

    result = list(filtered_products.iterate())

    assert len(result) == 1

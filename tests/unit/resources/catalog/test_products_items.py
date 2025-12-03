import pytest

from mpt_api_client.resources.catalog.products_items import (
    AsyncProductItemService,
    ProductItemService,
)


@pytest.fixture
def product_items_service(http_client):
    return ProductItemService(http_client=http_client, endpoint_params={"product_id": "PRD-001"})


@pytest.fixture
def async_product_items_service(async_http_client):
    return AsyncProductItemService(
        http_client=async_http_client, endpoint_params={"product_id": "PRD-001"}
    )


def test_endpoint(product_items_service):
    result = product_items_service.path == "/public/v1/catalog/products/PRD-001/items"

    assert result is True


def test_async_endpoint(async_product_items_service):
    result = async_product_items_service.path == "/public/v1/catalog/products/PRD-001/items"

    assert result is True


@pytest.mark.parametrize("method", ["get", "iterate"])
def test_methods_present(product_items_service, method):
    result = hasattr(product_items_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "iterate"])
def test_async_methods_present(async_product_items_service, method):
    result = hasattr(async_product_items_service, method)

    assert result is True

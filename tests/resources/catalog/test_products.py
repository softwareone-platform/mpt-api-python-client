import pytest

from mpt_api_client.resources.catalog.products import AsyncProductsService, ProductsService


@pytest.fixture
def products_service(http_client):
    return ProductsService(http_client=http_client)


@pytest.fixture
def async_products_service(async_http_client):
    return AsyncProductsService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method", ["get", "create", "update", "delete", "review", "publish", "unpublish"]
)
def test_mixins_present(products_service, method):
    assert hasattr(products_service, method)


@pytest.mark.parametrize(
    "method", ["get", "create", "update", "delete", "review", "publish", "unpublish"]
)
def test_async_mixins_present(async_products_service, method):
    assert hasattr(async_products_service, method)

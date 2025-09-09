import pytest

from mpt_api_client.http import AsyncHTTPClient
from mpt_api_client.resources.catalog import AsyncCatalog, Catalog
from mpt_api_client.resources.catalog.products import AsyncProductsService, ProductsService


def test_catalog_init(http_client):
    catalog = Catalog(http_client=http_client)

    assert isinstance(catalog, Catalog)
    assert catalog.http_client is http_client


def test_catalog_products_multiple_calls(http_client):
    catalog = Catalog(http_client=http_client)

    products_service = catalog.products
    products_service_additional = catalog.products

    assert products_service is not products_service_additional
    assert isinstance(products_service, ProductsService)
    assert isinstance(products_service_additional, ProductsService)


def test_async_catalog_init(async_http_client: AsyncHTTPClient):
    catalog = AsyncCatalog(http_client=async_http_client)

    assert isinstance(catalog, AsyncCatalog)
    assert catalog.http_client is async_http_client


@pytest.mark.parametrize(
    ("attr_name", "expected"),
    [
        ("products", ProductsService),
    ],
)
def test_catalog_properties(http_client, attr_name, expected):
    catalog = Catalog(http_client=http_client)

    service = getattr(catalog, attr_name)

    assert isinstance(service, expected)


@pytest.mark.parametrize(
    ("attr_name", "expected"),
    [
        ("products", AsyncProductsService),
    ],
)
def test_async_catalog_properties(http_client, attr_name, expected):
    catalog = AsyncCatalog(http_client=http_client)

    service = getattr(catalog, attr_name)

    assert isinstance(service, expected)

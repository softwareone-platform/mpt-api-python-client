import pytest

from mpt_api_client.resources.catalog.authorizations import (
    AsyncAuthorizationsService,
    AuthorizationsService,
)
from mpt_api_client.resources.catalog.catalog import AsyncCatalog, Catalog
from mpt_api_client.resources.catalog.items import AsyncItemsService, ItemsService
from mpt_api_client.resources.catalog.listings import AsyncListingsService, ListingsService
from mpt_api_client.resources.catalog.price_lists import (
    AsyncPriceListsService,
    PriceListsService,
)
from mpt_api_client.resources.catalog.products import AsyncProductsService, ProductsService
from mpt_api_client.resources.catalog.units_of_measure import (
    AsyncUnitsOfMeasureService,
    UnitsOfMeasureService,
)


@pytest.fixture
def catalog(http_client):
    return Catalog(http_client=http_client)


@pytest.fixture
def async_catalog(async_http_client):
    return AsyncCatalog(http_client=async_http_client)


@pytest.mark.parametrize(
    ("property_name", "expected_service_class"),
    [
        ("authorizations", AuthorizationsService),
        ("listings", ListingsService),
        ("price_lists", PriceListsService),
        ("products", ProductsService),
        ("units_of_measure", UnitsOfMeasureService),
        ("items", ItemsService),
    ],
)
def test_catalog_properties(catalog, property_name, expected_service_class):
    """Test that Catalog properties return correct instances."""
    service = getattr(catalog, property_name)

    assert isinstance(service, expected_service_class)
    assert service.http_client is catalog.http_client


@pytest.mark.parametrize(
    ("property_name", "expected_service_class"),
    [
        ("authorizations", AsyncAuthorizationsService),
        ("listings", AsyncListingsService),
        ("price_lists", AsyncPriceListsService),
        ("products", AsyncProductsService),
        ("units_of_measure", AsyncUnitsOfMeasureService),
        ("items", AsyncItemsService),
    ],
)
def test_async_catalog_properties(async_catalog, property_name, expected_service_class):
    """Test that AsyncCatalog properties return correct instances."""
    service = getattr(async_catalog, property_name)

    assert isinstance(service, expected_service_class)
    assert service.http_client is async_catalog.http_client


def test_catalog_initialization(http_client):
    """Test that Catalog can be properly initialized with http_client."""
    catalog = Catalog(http_client=http_client)

    assert catalog.http_client is http_client
    assert isinstance(catalog, Catalog)


def test_async_catalog_initialization(async_http_client):
    """Test that AsyncCatalog can be properly initialized with http_client."""
    async_catalog = AsyncCatalog(http_client=async_http_client)

    assert async_catalog.http_client is async_http_client
    assert isinstance(async_catalog, AsyncCatalog)

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
from mpt_api_client.resources.catalog.pricing_policies import (
    AsyncPricingPoliciesService,
    PricingPoliciesService,
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
        ("pricing_policies", PricingPoliciesService),
        ("products", ProductsService),
        ("units_of_measure", UnitsOfMeasureService),
        ("items", ItemsService),
    ],
)
def test_catalog_properties(catalog, property_name, expected_service_class):
    result = getattr(catalog, property_name)

    assert isinstance(result, expected_service_class)
    assert result.http_client is catalog.http_client


@pytest.mark.parametrize(
    ("property_name", "expected_service_class"),
    [
        ("authorizations", AsyncAuthorizationsService),
        ("listings", AsyncListingsService),
        ("price_lists", AsyncPriceListsService),
        ("pricing_policies", AsyncPricingPoliciesService),
        ("products", AsyncProductsService),
        ("units_of_measure", AsyncUnitsOfMeasureService),
        ("items", AsyncItemsService),
    ],
)
def test_async_catalog_properties(async_catalog, property_name, expected_service_class):
    result = getattr(async_catalog, property_name)

    assert isinstance(result, expected_service_class)
    assert result.http_client is async_catalog.http_client


def test_catalog_initialization(http_client):
    result = Catalog(http_client=http_client)

    assert result.http_client is http_client
    assert isinstance(result, Catalog)


def test_async_catalog_initialization(async_http_client):
    result = AsyncCatalog(http_client=async_http_client)

    assert result.http_client is async_http_client
    assert isinstance(result, AsyncCatalog)

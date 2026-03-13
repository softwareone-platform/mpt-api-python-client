import pytest

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.catalog.listings import (
    AsyncListingsService,
    Listing,
    ListingsService,
)


@pytest.fixture
def listings_service(http_client):
    return ListingsService(http_client=http_client)


@pytest.fixture
def async_listings_service(async_http_client):
    return AsyncListingsService(http_client=async_http_client)


@pytest.fixture
def listing_data():
    return {
        "id": "LST-001",
        "authorization": {"id": "AUT-001", "name": "My Auth"},
        "product": {"id": "PRD-001", "name": "My Product"},
        "vendor": {"id": "ACC-001", "name": "Vendor"},
        "seller": {"id": "ACC-002", "name": "Seller"},
        "priceList": {"id": "PRC-001", "currency": "USD"},
        "primary": True,
        "notes": "Some notes",
        "statistics": {"items": 3},
        "eligibility": {"status": "Eligible"},
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate"])
def test_mixins_present(listings_service, method):
    result = hasattr(listings_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate"])
def test_async_mixins_present(async_listings_service, method):
    result = hasattr(async_listings_service, method)

    assert result is True


def test_listing_primitive_fields(listing_data):
    result = Listing(listing_data)

    assert result.to_dict() == listing_data


def test_listing_nested_base_models(listing_data):
    result = Listing(listing_data)

    assert isinstance(result.authorization, BaseModel)
    assert isinstance(result.product, BaseModel)
    assert isinstance(result.price_list, BaseModel)
    assert isinstance(result.statistics, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_listing_optional_fields_absent():
    result = Listing({"id": "LST-001"})

    assert result.id == "LST-001"
    assert not hasattr(result, "notes")
    assert not hasattr(result, "primary")
    assert not hasattr(result, "audit")

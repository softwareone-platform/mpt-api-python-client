import pytest

from mpt_api_client.resources.catalog.listings import (
    AsyncListingsService,
    ListingsService,
)


@pytest.fixture
def listings_service(http_client):
    return ListingsService(http_client=http_client)


@pytest.fixture
def async_listings_service(async_http_client):
    return AsyncListingsService(http_client=async_http_client)


@pytest.mark.parametrize("method", ["get", "create", "update", "delete"])
def test_mixins_present(listings_service, method):
    assert hasattr(listings_service, method)


@pytest.mark.parametrize("method", ["get", "create", "update", "delete"])
def test_async_mixins_present(async_listings_service, method):
    assert hasattr(async_listings_service, method)

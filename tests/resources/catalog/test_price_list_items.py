import pytest

from mpt_api_client.resources.catalog.price_list_items import (
    AsyncPriceListItemsService,
    PriceListItemsService,
)


@pytest.fixture
def price_list_items_service(http_client):
    return PriceListItemsService(
        http_client=http_client, endpoint_params={"price_list_id": "ITM-0000-0001"}
    )


@pytest.fixture
def async_price_list_items_service(async_http_client):
    return AsyncPriceListItemsService(
        http_client=async_http_client, endpoint_params={"price_list_id": "ITM-0000-0001"}
    )


@pytest.fixture
def test_endpoint(price_list_items_service):
    assert price_list_items_service.endpoint == "/public/v1/catalog/price-lists/ITM-0000-0001/items"


@pytest.fixture
def async_test_endpoint(async_price_list_items_service):
    assert async_price_list_items_service.endpoint == (
        "/public/v1/catalog/price-lists/ITM-0000-0001/items"
    )


@pytest.mark.parametrize("method", ["get", "create", "delete", "update"])
def test_methods_present(price_list_items_service, method):
    assert hasattr(price_list_items_service, method)


@pytest.mark.parametrize("method", ["get", "create", "delete", "update"])
def test_async_methods_present(async_price_list_items_service, method):
    assert hasattr(async_price_list_items_service, method)

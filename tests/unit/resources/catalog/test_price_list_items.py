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
    result = price_list_items_service.path == "/public/v1/catalog/price-lists/ITM-0000-0001/items"

    assert result is True


@pytest.fixture
def async_test_endpoint(async_price_list_items_service):
    result = async_price_list_items_service.path == (
        "/public/v1/catalog/price-lists/ITM-0000-0001/items"
    )

    assert result is True


@pytest.mark.parametrize("method", ["get", "update", "iterate"])
def test_methods_present(price_list_items_service, method):
    result = hasattr(price_list_items_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "update", "iterate"])
def test_async_methods_present(async_price_list_items_service, method):
    result = hasattr(async_price_list_items_service, method)

    assert result is True

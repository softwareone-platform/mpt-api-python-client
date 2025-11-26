import pytest

from mpt_api_client.resources.catalog.price_list_items import (
    AsyncPriceListItemsService,
    PriceListItemsService,
)
from mpt_api_client.resources.catalog.price_lists import (
    AsyncPriceListsService,
    PriceListsService,
)


@pytest.fixture
def price_lists_service(http_client):
    return PriceListsService(http_client=http_client)


@pytest.fixture
def async_price_lists_service(http_client):
    return AsyncPriceListsService(http_client=http_client)


@pytest.mark.parametrize("method", ["get", "create", "update", "delete"])
def test_mixins_present(price_lists_service, method):
    result = hasattr(price_lists_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete"])
def test_async_mixins_present(async_price_lists_service, method):
    result = hasattr(async_price_lists_service, method)

    assert result is True


@pytest.mark.parametrize(
    ("service_method", "expected_model_class"),
    [
        ("items", PriceListItemsService),
    ],
)
def test_property_services(price_lists_service, service_method, expected_model_class):
    result = getattr(price_lists_service, service_method)("ITM-0000-0001")

    assert isinstance(result, expected_model_class)
    assert result.endpoint_params == {"price_list_id": "ITM-0000-0001"}


@pytest.mark.parametrize(
    ("service_method", "expected_model_class"),
    [
        ("items", AsyncPriceListItemsService),
    ],
)
def test_async_property_services(async_price_lists_service, service_method, expected_model_class):
    result = getattr(async_price_lists_service, service_method)("ITM-0000-0001")

    assert isinstance(result, expected_model_class)
    assert result.endpoint_params == {"price_list_id": "ITM-0000-0001"}

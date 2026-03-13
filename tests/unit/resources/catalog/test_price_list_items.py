import pytest

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.catalog.price_list_items import (
    AsyncPriceListItemsService,
    PriceListItem,
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
def price_list_item_data():
    return {
        "id": "PLI-001",
        "status": "Active",
        "description": "Item description",
        "reasonForChange": "Price update",
        "unitLP": 100.0,
        "unitPP": 80.0,
        "markup": 25.0,
        "margin": 20.0,
        "unitSP": 90.0,
        "PPx1": 80.0,
        "PPxM": 7.0,
        "PPxY": 84.0,
        "SPx1": 90.0,
        "SPxM": 8.0,
        "SPxY": 96.0,
        "LPx1": 100.0,
        "LPxM": 9.0,
        "LPxY": 108.0,
        "priceList": {"id": "PRC-001", "currency": "USD"},
        "item": {"id": "ITM-001", "name": "My Item"},
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


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


def test_price_list_item_primitive_fields(price_list_item_data):
    result = PriceListItem(price_list_item_data)

    assert result.to_dict() == price_list_item_data


def test_price_list_item_price_fields(price_list_item_data):
    result = PriceListItem(price_list_item_data)

    assert result.unit_lp == pytest.approx(100.0)
    assert result.unit_pp == pytest.approx(80.0)
    assert result.unit_sp == pytest.approx(90.0)
    assert result.spxm == pytest.approx(8.0)
    assert result.lpx1 == pytest.approx(100.0)


def test_price_list_item_nested_models(price_list_item_data):
    result = PriceListItem(price_list_item_data)

    assert isinstance(result.price_list, BaseModel)
    assert isinstance(result.item, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_price_list_item_optional_fields_absent():
    result = PriceListItem({"id": "PLI-001"})

    assert result.id == "PLI-001"
    assert not hasattr(result, "status")
    assert not hasattr(result, "unit_lp")
    assert not hasattr(result, "audit")

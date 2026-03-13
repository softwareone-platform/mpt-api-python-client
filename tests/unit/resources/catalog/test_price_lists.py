import pytest

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.catalog.price_list_items import (
    AsyncPriceListItemsService,
    PriceListItemsService,
)
from mpt_api_client.resources.catalog.price_lists import (
    AsyncPriceListsService,
    PriceList,
    PriceListsService,
)


@pytest.fixture
def price_lists_service(http_client):
    return PriceListsService(http_client=http_client)


@pytest.fixture
def async_price_lists_service(http_client):
    return AsyncPriceListsService(http_client=http_client)


@pytest.fixture
def price_list_data():
    return {
        "id": "PRC-001",
        "currency": "USD",
        "precision": 2,
        "defaultMarkup": 25.0,
        "defaultMargin": 20.0,
        "notes": "Some notes",
        "externalIds": {"vendor": "ext-001"},
        "statistics": {"items": 10},
        "product": {"id": "PRD-001", "name": "My Product"},
        "vendor": {"id": "ACC-001", "name": "Vendor"},
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate"])
def test_mixins_present(price_lists_service, method):
    result = hasattr(price_lists_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate"])
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


def test_price_list_primitive_fields(price_list_data):
    result = PriceList(price_list_data)

    assert result.to_dict() == price_list_data


def test_price_list_nested_fields_are_base_models(price_list_data):
    result = PriceList(price_list_data)

    assert isinstance(result.external_ids, BaseModel)
    assert isinstance(result.statistics, BaseModel)
    assert isinstance(result.product, BaseModel)
    assert isinstance(result.vendor, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_price_list_optional_fields_absent():
    result = PriceList({"id": "PRC-001"})

    assert result.id == "PRC-001"
    assert not hasattr(result, "currency")
    assert not hasattr(result, "precision")
    assert not hasattr(result, "audit")

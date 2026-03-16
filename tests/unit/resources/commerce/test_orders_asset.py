import pytest

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.commerce.orders_asset import (
    AsyncOrdersAssetService,
    OrdersAsset,
    OrdersAssetService,
)


@pytest.fixture
def asset_service(http_client):
    return OrdersAssetService(http_client=http_client, endpoint_params={"order_id": "ORD-123"})


@pytest.fixture
def async_asset_service(async_http_client):
    return AsyncOrdersAssetService(
        http_client=async_http_client, endpoint_params={"order_id": "ORD-123"}
    )


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "render"])
def test_mixins_present(asset_service, method):
    result = hasattr(asset_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "render"])
def test_async_mixins_present(async_asset_service, method):
    result = hasattr(async_asset_service, method)

    assert result is True


def test_endpoint(asset_service):
    result = asset_service.path == "/public/v1/commerce/orders/ORD-123/assets"

    assert result is True


def test_async_endpoint(async_asset_service):
    result = async_asset_service.path == "/public/v1/commerce/orders/ORD-123/assets"

    assert result is True


@pytest.fixture
def orders_asset_data():
    return {
        "id": "ASS-001",
        "name": "Order Asset",
        "status": "Active",
        "externalIds": {"vendor": "ext-001"},
        "price": {"total": 100},
        "template": {"id": "TPL-001"},
        "parameters": {"fulfillment": []},
        "terms": {"id": "TRM-001"},
        "lines": [{"id": "LIN-001"}],
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


def test_orders_asset_primitive_fields(orders_asset_data):
    result = OrdersAsset(orders_asset_data)

    assert result.to_dict() == orders_asset_data


def test_orders_asset_nested_fields(orders_asset_data):  # noqa: WPS218
    result = OrdersAsset(orders_asset_data)

    assert isinstance(result.external_ids, BaseModel)
    assert isinstance(result.price, BaseModel)
    assert isinstance(result.template, BaseModel)
    assert isinstance(result.parameters, BaseModel)
    assert isinstance(result.terms, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_orders_asset_optional_fields_absent():
    result = OrdersAsset({"id": "ASS-001"})

    assert result.id == "ASS-001"
    assert not hasattr(result, "name")
    assert not hasattr(result, "status")
    assert not hasattr(result, "audit")

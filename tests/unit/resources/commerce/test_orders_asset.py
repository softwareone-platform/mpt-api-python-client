import pytest

from mpt_api_client.resources.commerce.orders_asset import (
    AsyncOrdersAssetService,
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

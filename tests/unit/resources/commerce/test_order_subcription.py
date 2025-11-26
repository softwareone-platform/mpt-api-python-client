import pytest

from mpt_api_client.resources.commerce.orders_subscription import (
    AsyncOrderSubscriptionsService,
    OrderSubscriptionsService,
)


@pytest.fixture
def subscription_service(http_client):
    return OrderSubscriptionsService(
        http_client=http_client, endpoint_params={"order_id": "ORD-123"}
    )


@pytest.fixture
def async_subscription_service(async_http_client):
    return AsyncOrderSubscriptionsService(
        http_client=async_http_client, endpoint_params={"order_id": "ORD-123"}
    )


@pytest.mark.parametrize("method", ["get", "create", "delete", "update"])
def test_mixins_present(subscription_service, method):
    result = hasattr(subscription_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "delete", "update"])
def test_async_mixins_present(async_subscription_service, method):
    result = hasattr(async_subscription_service, method)

    assert result is True


def test_endpoint(subscription_service):
    result = subscription_service.path == "/public/v1/commerce/orders/ORD-123/subscriptions"

    assert result is True


def test_async_endpoint(async_subscription_service):
    result = async_subscription_service.path == "/public/v1/commerce/orders/ORD-123/subscriptions"

    assert result is True

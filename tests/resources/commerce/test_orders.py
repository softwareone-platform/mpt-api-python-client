import httpx
import pytest
import respx

from mpt_api_client.resources.commerce.orders import AsyncOrdersService, OrdersService
from mpt_api_client.resources.commerce.orders_subscription import (
    AsyncOrderSubscriptionsService,
    OrderSubscriptionsService,
)


@pytest.fixture
def orders_service(http_client):
    return OrdersService(http_client=http_client)


@pytest.fixture
def async_orders_service(async_http_client):
    return AsyncOrdersService(http_client=async_http_client)


def test_notify(orders_service):
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/commerce/orders/ORD-123/notify"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "application/json"},
                content='{"status": "notified"}',
            )
        )
        user_data = {"email": "user@example.com", "name": "John Doe"}

        orders_service.notify("ORD-123", user_data)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == b'{"email":"user@example.com","name":"John Doe"}'


async def test_async_notify(async_orders_service):
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/commerce/orders/ORD-123/notify"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "application/json"},
                content='{"status": "notified"}',
            )
        )
        user_data = {"email": "user@example.com", "name": "John Doe"}

        await async_orders_service.notify("ORD-123", user_data)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == b'{"email":"user@example.com","name":"John Doe"}'


def test_subscription_service(http_client):
    orders_service = OrdersService(http_client=http_client)

    subscriptions = orders_service.subscriptions("ORD-123")

    assert isinstance(subscriptions, OrderSubscriptionsService)
    assert subscriptions.endpoint_params == {"order_id": "ORD-123"}


def test_async_subscription_service(async_http_client):
    orders_service = AsyncOrdersService(http_client=async_http_client)

    subscriptions = orders_service.subscriptions("ORD-123")

    assert isinstance(subscriptions, AsyncOrderSubscriptionsService)
    assert subscriptions.endpoint_params == {"order_id": "ORD-123"}


@pytest.mark.parametrize(
    "method",
    [
        "get",
        "create",
        "update",
        "delete",
        "validate",
        "process",
        "query",
        "complete",
        "fail",
        "template",
    ],
)
def test_mixins_present(orders_service, method):
    assert hasattr(orders_service, method)


@pytest.mark.parametrize(
    "method",
    [
        "get",
        "create",
        "update",
        "delete",
        "validate",
        "process",
        "query",
        "complete",
        "fail",
        "template",
    ],
)
def test_async_mixins_present(async_orders_service, method):
    assert hasattr(async_orders_service, method)

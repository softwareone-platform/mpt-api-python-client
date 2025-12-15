import httpx
import pytest
import respx

from mpt_api_client.resources.commerce.orders import AsyncOrdersService, Order, OrdersService
from mpt_api_client.resources.commerce.orders_asset import (
    AsyncOrdersAssetService,
    OrdersAssetService,
)
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


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("validate", {"id": "ORD-123", "status": "update"}),
        ("process", {"id": "ORD-123", "status": "update"}),
        ("query", {"id": "ORD-123", "status": "update"}),
        ("complete", {"id": "ORD-123", "status": "update"}),
        ("fail", {"id": "ORD-123", "status": "update"}),
        ("quote", {"id": "ORD-123", "status": "update"}),
    ],
)
def test_custom_resource_actions(orders_service, action, input_status):
    request_expected_content = b'{"id":"ORD-123","status":"update"}'
    response_expected_data = {"id": "ORD-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/commerce/orders/ORD-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = getattr(orders_service, action)("ORD-123", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, Order)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("validate", None),
        ("process", None),
        ("query", None),
        ("complete", None),
        ("fail", None),
        ("quote", None),
    ],
)
def test_custom_resource_actions_no_data(orders_service, action, input_status):
    request_expected_content = b""
    response_expected_data = {"id": "ORD-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/commerce/orders/ORD-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = getattr(orders_service, action)("ORD-123")

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, Order)


def test_notify(orders_service):
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/commerce/orders/ORD-123/notify"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                content='{"status": "notified"}',
            )
        )
        user_data = {"email": "user@example.com", "name": "John Doe"}

        orders_service.notify("ORD-123", user_data)  # act

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == b'{"email":"user@example.com","name":"John Doe"}'


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("validate", {"id": "ORD-123", "status": "update"}),
        ("process", {"id": "ORD-123", "status": "update"}),
        ("query", {"id": "ORD-123", "status": "update"}),
        ("complete", {"id": "ORD-123", "status": "update"}),
        ("fail", {"id": "ORD-123", "status": "update"}),
        ("quote", {"id": "ORD-123", "status": "update"}),
    ],
)
async def test_async_custom_resource_actions(async_orders_service, action, input_status):
    request_expected_content = b'{"id":"ORD-123","status":"update"}'
    response_expected_data = {"id": "ORD-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/commerce/orders/ORD-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await getattr(async_orders_service, action)("ORD-123", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, Order)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("validate", None),
        ("process", None),
        ("query", None),
        ("complete", None),
        ("fail", None),
        ("quote", None),
    ],
)
async def test_async_custom_resource_actions_nodata(async_orders_service, action, input_status):
    request_expected_content = b""
    response_expected_data = {"id": "ORD-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/commerce/orders/ORD-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await getattr(async_orders_service, action)("ORD-123")

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, Order)


async def test_async_notify(async_orders_service):
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/commerce/orders/ORD-123/notify"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                content='{"status": "notified"}',
            )
        )
        user_data = {"email": "user@example.com", "name": "John Doe"}

        await async_orders_service.notify("ORD-123", user_data)  # act

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == b'{"email":"user@example.com","name":"John Doe"}'


def test_subscription_service(http_client):
    orders_service = OrdersService(http_client=http_client)

    result = orders_service.subscriptions("ORD-123")

    assert isinstance(result, OrderSubscriptionsService)
    assert result.endpoint_params == {"order_id": "ORD-123"}


def test_async_subscription_service(async_http_client):
    orders_service = AsyncOrdersService(http_client=async_http_client)

    result = orders_service.subscriptions("ORD-123")

    assert isinstance(result, AsyncOrderSubscriptionsService)
    assert result.endpoint_params == {"order_id": "ORD-123"}


def test_asset_service(http_client):
    orders_service = OrdersService(http_client=http_client)

    result = orders_service.assets("ORD-123")

    assert isinstance(result, OrdersAssetService)
    assert result.endpoint_params == {"order_id": "ORD-123"}


def test_async_asset_service(async_http_client):
    orders_service = AsyncOrdersService(http_client=async_http_client)

    result = orders_service.assets("ORD-123")

    assert isinstance(result, AsyncOrdersAssetService)
    assert result.endpoint_params == {"order_id": "ORD-123"}


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "render", "template"])
def test_mixins_present(orders_service, method):
    result = hasattr(orders_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "render", "template"])
def test_async_mixins_present(async_orders_service, method):
    result = hasattr(async_orders_service, method)

    assert result is True

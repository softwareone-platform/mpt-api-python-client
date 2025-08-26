import httpx
import pytest
import respx

from mpt_api_client.resources.commerce.orders import AsyncOrdersService, Order, OrdersService


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
        ("validate", None),
        ("process", {"id": "ORD-123", "status": "update"}),
        ("process", None),
        ("query", {"id": "ORD-123", "status": "update"}),
        ("query", None),
        ("complete", {"id": "ORD-123", "status": "update"}),
        ("complete", None),
        ("fail", {"id": "ORD-123", "status": "update"}),
        ("fail", None),
    ],
)
def test_custom_resource_actions(orders_service, action, input_status):
    if input_status is None:
        request_expected_content = b""
    else:
        request_expected_content = b'{"id":"ORD-123","status":"update"}'
    response_expected_data = {"id": "ORD-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/commerce/orders/ORD-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        if input_status is None:
            order = getattr(orders_service, action)("ORD-123")
        else:
            order = getattr(orders_service, action)("ORD-123", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        if input_status is None:
            assert request.content == request_expected_content
        else:
            assert request.content == request_expected_content
        assert order.to_dict() == response_expected_data
        assert isinstance(order, Order)


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


def test_template(orders_service):
    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/public/v1/commerce/orders/ORD-123/template"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "text/markdown"},
                content="# Order Template\n\nThis is a markdown template.",
            )
        )

        markdown_template = orders_service.template("ORD-123")

        assert mock_route.called
        assert mock_route.call_count == 1
        assert markdown_template == "# Order Template\n\nThis is a markdown template."


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("validate", {"id": "ORD-123", "status": "update"}),
        ("validate", None),
        ("process", {"id": "ORD-123", "status": "update"}),
        ("process", None),
        ("query", {"id": "ORD-123", "status": "update"}),
        ("query", None),
        ("complete", {"id": "ORD-123", "status": "update"}),
        ("complete", None),
        ("fail", {"id": "ORD-123", "status": "update"}),
        ("fail", None),
    ],
)
@pytest.mark.asyncio
async def test_async_custom_resource_actions(async_orders_service, action, input_status):
    if input_status is None:
        request_expected_content = b""
    else:
        request_expected_content = b'{"id":"ORD-123","status":"update"}'
    response_expected_data = {"id": "ORD-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/commerce/orders/ORD-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        if input_status is None:
            order = await getattr(async_orders_service, action)("ORD-123")
        else:
            order = await getattr(async_orders_service, action)("ORD-123", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        if input_status is None:
            assert request.content == request_expected_content
        else:
            assert request.content == request_expected_content
        assert order.to_dict() == response_expected_data
        assert isinstance(order, Order)


@pytest.mark.asyncio
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


@pytest.mark.asyncio
async def test_async_template(async_orders_service):
    template_content = "# Order Template\n\nThis is a markdown template."
    with respx.mock:
        respx.get("https://api.example.com/public/v1/commerce/orders/ORD-123/template").mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "text/markdown"},
                content=template_content,
            )
        )

        template = await async_orders_service.template("ORD-123")

        assert template == template_content

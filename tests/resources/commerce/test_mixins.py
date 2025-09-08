import httpx
import pytest
import respx

from mpt_api_client.resources.commerce.orders import AsyncOrdersService, Order, OrdersService


@pytest.fixture
def dummy_service(http_client):
    return OrdersService(http_client=http_client)


@pytest.fixture
def async_dummy_service(async_http_client):
    return AsyncOrdersService(http_client=async_http_client)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("validate", {"id": "ORD-123", "status": "update"}),
        ("process", {"id": "ORD-123", "status": "update"}),
        ("query", {"id": "ORD-123", "status": "update"}),
        ("complete", {"id": "ORD-123", "status": "update"}),
        ("fail", {"id": "ORD-123", "status": "update"}),
    ],
)
def test_custom_resource_actions(dummy_service, action, input_status):
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
        order = getattr(dummy_service, action)("ORD-123", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert order.to_dict() == response_expected_data
        assert isinstance(order, Order)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("validate", None),
        ("process", None),
        ("query", None),
        ("complete", None),
        ("fail", None),
    ],
)
def test_custom_resource_actions_no_data(dummy_service, action, input_status):
    request_expected_content = b""
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

        order = getattr(dummy_service, action)("ORD-123")

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert order.to_dict() == response_expected_data
        assert isinstance(order, Order)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("validate", {"id": "ORD-123", "status": "update"}),
        ("process", {"id": "ORD-123", "status": "update"}),
        ("query", {"id": "ORD-123", "status": "update"}),
        ("complete", {"id": "ORD-123", "status": "update"}),
        ("fail", {"id": "ORD-123", "status": "update"}),
    ],
)
async def test_async_custom_resource_actions(async_dummy_service, action, input_status):
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
        order = await getattr(async_dummy_service, action)("ORD-123", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert order.to_dict() == response_expected_data
        assert isinstance(order, Order)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("validate", None),
        ("process", None),
        ("query", None),
        ("complete", None),
        ("fail", None),
    ],
)
async def test_async_custom_resource_actions_nodata(async_dummy_service, action, input_status):
    request_expected_content = b""
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
        order = await getattr(async_dummy_service, action)("ORD-123")

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert order.to_dict() == response_expected_data
        assert isinstance(order, Order)


def test_template(dummy_service):
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

        markdown_template = dummy_service.template("ORD-123")

        assert mock_route.called
        assert mock_route.call_count == 1
        assert markdown_template == "# Order Template\n\nThis is a markdown template."


async def test_async_template(async_dummy_service):
    template_content = "# Order Template\n\nThis is a markdown template."
    with respx.mock:
        respx.get("https://api.example.com/public/v1/commerce/orders/ORD-123/template").mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "text/markdown"},
                content=template_content,
            )
        )

        template = await async_dummy_service.template("ORD-123")

        assert template == template_content

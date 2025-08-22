import httpx
import pytest
import respx

from mpt_api_client.resources.order import Order, OrderResourceClient


@pytest.fixture
def order_client(mpt_client):
    return OrderResourceClient(mpt_client, "ORD-123")


@pytest.mark.parametrize(
    ("action", "input_status", "expected_content"),
    [
        ("validate", "draft", b'{"id":"ORD-123","status":"draft"}'),
        ("process", "processing", b'{"id":"ORD-123","status":"processing"}'),
        ("query", "querying", b'{"id":"ORD-123","status":"querying"}'),
        ("complete", "completed", b'{"id":"ORD-123","status":"completed"}'),
        ("fail", "failed", b'{"id":"ORD-123","status":"failed"}'),
    ],
)
def test_custom_resource_actions(order_client, action, input_status, expected_content):
    with respx.mock:
        order_data = {"id": "ORD-123", "status": input_status}
        mock_route = respx.post(
            f"https://api.example.com/public/v1/commerce/orders/ORD-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "application/json"},
                json={"id": "ORD-123", "status": input_status},
            )
        )

        order = getattr(order_client, action)(order_data)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == expected_content
        assert isinstance(order, Order)


def test_notify(order_client):
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

        order_client.notify(user_data)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == b'{"email":"user@example.com","name":"John Doe"}'


def test_template(mpt_client):
    order_client = OrderResourceClient(mpt_client, "ORD-123")

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

        markdown_template = order_client.template()

        assert mock_route.called
        assert mock_route.call_count == 1
        assert markdown_template == "# Order Template\n\nThis is a markdown template."

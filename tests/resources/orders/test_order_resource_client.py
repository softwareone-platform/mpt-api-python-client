from unittest.mock import Mock, patch

import httpx
import pytest

from mpt_api_client.resources.order import Order, OrderResourceClient


@pytest.fixture
def order_response():
    return httpx.Response(
        status_code=200,
        headers={"content-type": "application/json"},
        content='{"id": "order123", "status": "completed", "$meta": {"total": 1}}',
        request=httpx.Request("POST", "https://api.example.com/orders"),
    )


@pytest.fixture
def order_client():
    with patch.object(OrderResourceClient, "do_action"):
        client = OrderResourceClient(Mock(), "order123")
        yield client


def test_validate(order_client, order_response):
    order_client.do_action.return_value = order_response
    order_data = {"id": "order123", "status": "draft"}

    order = order_client.validate(order_data)

    order_client.do_action.assert_called_once_with("POST", "validate", json=order_data)
    assert isinstance(order, Order)


def test_process(order_client, order_response):
    order_client.do_action.return_value = order_response
    order_data = {"id": "order123", "status": "validated"}

    order = order_client.process(order_data)

    order_client.do_action.assert_called_once_with("POST", "process", json=order_data)
    assert isinstance(order, Order)


def test_query(order_client, order_response):
    order_client.do_action.return_value = order_response
    order_data = {"id": "order123", "status": "processing"}

    order = order_client.query(order_data)

    order_client.do_action.assert_called_once_with("POST", "query", json=order_data)
    assert isinstance(order, Order)


def test_complete(order_client, order_response):
    order_client.do_action.return_value = order_response
    order_data = {"id": "order123", "status": "processing"}

    order = order_client.complete(order_data)

    order_client.do_action.assert_called_once_with("POST", "complete", json=order_data)
    assert isinstance(order, Order)


def test_fail(order_client, order_response):
    order_client.do_action.return_value = order_response
    order_data = {"id": "order123", "status": "processing"}

    order = order_client.fail(order_data)

    order_client.do_action.assert_called_once_with("POST", "fail", json=order_data)
    assert isinstance(order, Order)


def test_notify(order_client, order_response):
    order_client.do_action.return_value = order_response
    user_data = {"email": "user@example.com", "name": "John Doe"}

    order_client.notify(user_data)

    order_client.do_action.assert_called_once_with("POST", "notify", json=user_data)


def test_template(order_client):
    template_response = httpx.Response(
        status_code=200,
        headers={"content-type": "text/markdown"},
        content="# Order Template\n\nThis is a markdown template.",
        request=httpx.Request("GET", "https://api.example.com/orders/template"),
    )
    order_client.do_action.return_value = template_response

    markdown_template = order_client.template()

    order_client.do_action.assert_called_once_with("GET", "template")
    assert markdown_template == "# Order Template\n\nThis is a markdown template."

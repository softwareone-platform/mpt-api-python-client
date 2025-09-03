import httpx
import pytest
import respx

from mpt_api_client.resources.commerce.subscriptions import (
    AsyncSubscriptionsService,
    SubscriptionsService,
)


@pytest.fixture
def subscriptions_service(http_client):
    return SubscriptionsService(http_client=http_client)


@pytest.fixture
def async_subscriptions_service(async_http_client):
    return AsyncSubscriptionsService(http_client=async_http_client)


async def test_async_terminate(async_subscriptions_service):
    subscription_expected = {"id": "SUB-123", "status": "Terminated", "name": "Terminated SUB-123"}
    with respx.mock:
        respx.post(
            "https://api.example.com/public/v1/commerce/subscriptions/SUB-123/terminate"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=subscription_expected,
            )
        )

        subscription_updated = await async_subscriptions_service.terminate(
            "SUB-123", {"name": "Terminated SUB-123"}
        )

        assert subscription_updated.to_dict() == subscription_expected


async def test_async_render(async_subscriptions_service):
    template_content = "# Subscription Template\n\nThis is a markdown template."
    with respx.mock:
        respx.get("https://api.example.com/public/v1/commerce/subscriptions/SUB-123/render").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "text/markdown"},
                content=template_content,
            )
        )

        template = await async_subscriptions_service.render("SUB-123")

        assert template == template_content


def test_terminate(subscriptions_service):
    subscription_expected = {"id": "SUB-123", "status": "Terminated", "name": "Terminated SUB-123"}
    with respx.mock:
        respx.post(
            "https://api.example.com/public/v1/commerce/subscriptions/SUB-123/terminate"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=subscription_expected,
            )
        )

        subscription_updated = subscriptions_service.terminate(
            "SUB-123", {"name": "Terminated SUB-123"}
        )

        assert subscription_updated.to_dict() == subscription_expected


def test_render(subscriptions_service):
    template_content = "# Subscription Template\n\nThis is a markdown template."
    with respx.mock:
        respx.get("https://api.example.com/public/v1/commerce/subscriptions/SUB-123/render").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "text/markdown"},
                content=template_content,
            )
        )

        template = subscriptions_service.render("SUB-123")

        assert template == template_content

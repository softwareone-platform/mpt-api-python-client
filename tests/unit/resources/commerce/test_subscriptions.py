import httpx
import pytest
import respx

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.commerce.subscriptions import (
    AsyncSubscriptionsService,
    Subscription,
    SubscriptionsService,
)


@pytest.fixture
def subscriptions_service(http_client):
    return SubscriptionsService(http_client=http_client)


@pytest.fixture
def async_subscriptions_service(async_http_client):
    return AsyncSubscriptionsService(http_client=async_http_client)


@pytest.mark.parametrize("method", ["get", "create", "update", "iterate", "terminate", "render"])
def test_methods_present(subscriptions_service, method):
    result = hasattr(subscriptions_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "iterate", "terminate", "render"])
def test_async_methods_present(async_subscriptions_service, method):
    result = hasattr(async_subscriptions_service, method)

    assert result is True


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

        result = subscriptions_service.terminate("SUB-123", {"name": "Terminated SUB-123"})

        assert result.to_dict() == subscription_expected


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

        result = subscriptions_service.render("SUB-123")

        assert result == template_content


@pytest.fixture
def subscription_data():
    return {
        "id": "SUB-001",
        "name": "My Subscription",
        "status": "Active",
        "startDate": "2024-01-01",
        "terminationDate": "2025-01-01",
        "commitmentDate": "2024-06-01",
        "splitStatus": "none",
        "autoRenew": True,
        "externalIds": {"vendor": "ext-001"},
        "terms": {"id": "TRM-001"},
        "product": {"id": "PRD-001"},
        "price": {"total": 100},
        "parameters": {"fulfillment": []},
        "agreement": {"id": "AGR-001"},
        "buyer": {"id": "ACC-001"},
        "licensee": {"id": "ACC-002"},
        "seller": {"id": "ACC-003"},
        "split": {"type": "none"},
        "template": {"id": "TPL-001"},
        "lines": [{"id": "LIN-001"}],
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


def test_subscription_primitive_fields(subscription_data):
    result = Subscription(subscription_data)

    assert result.to_dict() == subscription_data


def test_subscription_nested_core_fields(subscription_data):  # noqa: WPS218
    result = Subscription(subscription_data)

    assert isinstance(result.external_ids, BaseModel)
    assert isinstance(result.terms, BaseModel)
    assert isinstance(result.product, BaseModel)
    assert isinstance(result.price, BaseModel)
    assert isinstance(result.parameters, BaseModel)
    assert isinstance(result.agreement, BaseModel)


def test_subscription_nested_party_fields(subscription_data):  # noqa: WPS218
    result = Subscription(subscription_data)

    assert isinstance(result.buyer, BaseModel)
    assert isinstance(result.licensee, BaseModel)
    assert isinstance(result.seller, BaseModel)
    assert isinstance(result.split, BaseModel)
    assert isinstance(result.template, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_subscription_optional_fields_absent():
    result = Subscription({"id": "SUB-001"})

    assert result.id == "SUB-001"
    assert not hasattr(result, "name")
    assert not hasattr(result, "status")
    assert not hasattr(result, "audit")

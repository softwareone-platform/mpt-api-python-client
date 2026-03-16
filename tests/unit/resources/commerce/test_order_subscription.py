import pytest

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.commerce.orders_subscription import (
    AsyncOrderSubscriptionsService,
    OrderSubscription,
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


@pytest.fixture
def order_subscription_data():
    return {
        "id": "SUB-001",
        "name": "Order Subscription",
        "status": "Active",
        "startDate": "2024-01-01",
        "terminationDate": "2025-01-01",
        "commitmentDate": "2024-06-01",
        "autoRenew": True,
        "externalIds": {"vendor": "ext-001"},
        "terms": {"id": "TRM-001"},
        "product": {"id": "PRD-001"},
        "parameters": {"fulfillment": []},
        "agreement": {"id": "AGR-001"},
        "price": {"total": 100},
        "template": {"id": "TPL-001"},
        "lines": [{"id": "LIN-001"}],
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


def test_order_subscription_primitive_fields(order_subscription_data):
    result = OrderSubscription(order_subscription_data)

    assert result.to_dict() == order_subscription_data


def test_order_subscription_nested_fields(order_subscription_data):  # noqa: WPS218
    result = OrderSubscription(order_subscription_data)

    assert isinstance(result.external_ids, BaseModel)
    assert isinstance(result.terms, BaseModel)
    assert isinstance(result.product, BaseModel)
    assert isinstance(result.parameters, BaseModel)
    assert isinstance(result.agreement, BaseModel)
    assert isinstance(result.price, BaseModel)
    assert isinstance(result.template, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_order_subscription_fields_absent():
    result = OrderSubscription({"id": "SUB-001"})

    assert result.id == "SUB-001"
    assert not hasattr(result, "name")
    assert not hasattr(result, "status")
    assert not hasattr(result, "audit")

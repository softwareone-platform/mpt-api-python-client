import httpx
import pytest
import respx

from mpt_api_client.models.model import BaseModel
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


@pytest.fixture
def order_data():
    return {
        "id": "ORD-001",
        "type": "Purchase",
        "status": "Processing",
        "notes": "Some notes",
        "comments": "Some comments",
        "defaultMarkupSource": "standard",
        "statusNotes": {"reason": "pending review"},
        "template": {"id": "TPL-001"},
        "listing": {"id": "LST-001"},
        "authorization": {"id": "AUT-001"},
        "agreement": {"id": "AGR-001"},
        "assignee": {"id": "USR-001"},
        "externalIds": {"vendor": "ext-001"},
        "price": {"total": 100},
        "lines": [{"id": "LIN-001"}],
        "subscriptions": [{"id": "SUB-001"}],
        "assets": [{"id": "ASS-001"}],
        "parameters": {"fulfillment": []},
        "error": {"message": "some error"},
        "product": {"id": "PRD-001"},
        "client": {"id": "ACC-001"},
        "licensee": {"id": "ACC-002"},
        "buyer": {"id": "ACC-003"},
        "seller": {"id": "ACC-004"},
        "vendor": {"id": "ACC-005"},
        "billTo": {"address": "123 Main St"},
        "pricingPolicy": {"id": "PPL-001"},
        "termsAndConditions": [{"id": "TAC-001"}],
        "certificates": [{"id": "CRT-001"}],
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


def test_order_primitive_fields(order_data):
    result = Order(order_data)

    assert result.to_dict() == order_data


def test_order_nested_header_fields(order_data):  # noqa: WPS218
    result = Order(order_data)

    assert isinstance(result.status_notes, BaseModel)
    assert isinstance(result.template, BaseModel)
    assert isinstance(result.listing, BaseModel)
    assert isinstance(result.authorization, BaseModel)
    assert isinstance(result.agreement, BaseModel)


def test_order_nested_pricing_fields(order_data):  # noqa: WPS218
    result = Order(order_data)

    assert isinstance(result.assignee, BaseModel)
    assert isinstance(result.external_ids, BaseModel)
    assert isinstance(result.price, BaseModel)
    assert isinstance(result.parameters, BaseModel)
    assert isinstance(result.error, BaseModel)


def test_order_nested_party_fields(order_data):  # noqa: WPS218
    result = Order(order_data)

    assert isinstance(result.product, BaseModel)
    assert isinstance(result.client, BaseModel)
    assert isinstance(result.licensee, BaseModel)
    assert isinstance(result.buyer, BaseModel)
    assert isinstance(result.seller, BaseModel)


def test_order_nested_billing_fields(order_data):  # noqa: WPS218
    result = Order(order_data)

    assert isinstance(result.vendor, BaseModel)
    assert isinstance(result.bill_to, BaseModel)
    assert isinstance(result.pricing_policy, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_order_optional_fields_absent():
    result = Order({"id": "ORD-001"})

    assert result.id == "ORD-001"
    assert not hasattr(result, "type")
    assert not hasattr(result, "status")
    assert not hasattr(result, "audit")

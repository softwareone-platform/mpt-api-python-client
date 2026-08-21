import httpx
import pytest
import respx

from mpt_api_client.resources.notifications.webhooks import (
    AsyncWebhooksService,
    WebhooksService,
)


@pytest.fixture
def webhooks_service(http_client):
    return WebhooksService(http_client=http_client)


@pytest.fixture
def async_webhooks_service(async_http_client):
    return AsyncWebhooksService(http_client=async_http_client)


@pytest.fixture
def webhook_data():
    return {
        "id": "WH-1234",
        "name": "Order validation",
        "url": "https://example.com/hook",
        "description": "Validates draft orders",
        "status": "Enabled",
        "type": "ValidatePurchaseOrderDraft",
        "secret": "s3cret",
        "objectType": "Order",
        "account": {"id": "ACC-1234", "name": "Account"},
        "object": {"id": "PRD-1234", "name": "Product"},
        "criteria": [{"key": "product.id", "value": "PRD-1234"}],
        "statistics": {"total": 10, "failed": 1},
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


def test_endpoint(webhooks_service):
    result = webhooks_service.build_path()

    assert result == "/public/v1/notifications/webhooks"


def test_async_endpoint(async_webhooks_service):
    result = async_webhooks_service.build_path()

    assert result == "/public/v1/notifications/webhooks"


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "enable", "disable", "iterate", "fetch_page"],
)
def test_mixins_present(webhooks_service, method):
    result = hasattr(webhooks_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "enable", "disable", "iterate", "fetch_page"],
)
def test_async_mixins_present(async_webhooks_service, method):
    result = hasattr(async_webhooks_service, method)

    assert result is True


def test_get_webhook(webhooks_service, webhook_data):
    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/public/v1/notifications/webhooks/WH-1234"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "application/json"},
                json=webhook_data,
            )
        )

        result = webhooks_service.get("WH-1234")

        assert mock_route.call_count == 1
        assert result.to_dict() == webhook_data
        assert result.object_type == "Order"
        assert result.object.id == "PRD-1234"


@pytest.mark.parametrize("action", ["enable", "disable"])
def test_webhook_state_actions(webhooks_service, action):
    response_expected_data = {"id": "WH-1234", "status": "Enabled"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/notifications/webhooks/WH-1234/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = getattr(webhooks_service, action)("WH-1234")

        assert mock_route.call_count == 1
        assert result.to_dict() == response_expected_data


@pytest.mark.parametrize("action", ["enable", "disable"])
async def test_async_webhook_state_actions(async_webhooks_service, action):
    response_expected_data = {"id": "WH-1234", "status": "Enabled"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/notifications/webhooks/WH-1234/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await getattr(async_webhooks_service, action)("WH-1234")

        assert mock_route.call_count == 1
        assert result.to_dict() == response_expected_data

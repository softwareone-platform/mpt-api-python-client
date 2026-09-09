import httpx
import pytest
import respx

from mpt_api_client.resources.notifications.template_variants import (
    AsyncTemplateVariantsService,
    TemplateVariantsService,
)
from mpt_api_client.resources.notifications.templates import (
    AsyncTemplatesService,
    TemplatesService,
)


@pytest.fixture
def templates_service(http_client):
    return TemplatesService(http_client=http_client)


@pytest.fixture
def async_templates_service(async_http_client):
    return AsyncTemplatesService(http_client=async_http_client)


@pytest.fixture
def template_data():
    return {
        "id": "NTL-1234",
        "name": "Order confirmation",
        "description": "Sent when an order is completed",
        "status": "Active",
        "type": "Event",
        "externalId": "order-confirmation",
        "lastUsed": "2024-01-01T00:00:00Z",
        "category": {"id": "NCA-1234", "name": "Orders"},
        "defaultVariant": {"id": "NTV-1234", "languageCode": "en-US"},
        "owner": {"id": "ACC-1234", "name": "Account"},
        "variants": [{"id": "NTV-1234", "languageCode": "en-US"}],
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


def test_endpoint(templates_service):
    result = templates_service.build_path()

    assert result == "/public/v1/notifications/templates"


def test_async_endpoint(async_templates_service):
    result = async_templates_service.build_path()

    assert result == "/public/v1/notifications/templates"


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "activate", "disable", "iterate", "fetch_page"],
)
def test_mixins_present(templates_service, method):
    result = hasattr(templates_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "activate", "disable", "iterate", "fetch_page"],
)
def test_async_mixins_present(async_templates_service, method):
    result = hasattr(async_templates_service, method)

    assert result is True


def test_get_template(templates_service, template_data):
    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/public/v1/notifications/templates/NTL-1234"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "application/json"},
                json=template_data,
            )
        )

        result = templates_service.get("NTL-1234")

        assert mock_route.call_count == 1
        assert result.to_dict() == template_data
        assert result.external_id == "order-confirmation"
        assert result.default_variant.id == "NTV-1234"


@pytest.mark.parametrize("action", ["activate", "disable"])
def test_template_state_actions(templates_service, action):
    response_expected_data = {"id": "NTL-1234", "status": "Active"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/notifications/templates/NTL-1234/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = getattr(templates_service, action)("NTL-1234")

        assert mock_route.call_count == 1
        assert result.to_dict() == response_expected_data


@pytest.mark.parametrize("action", ["activate", "disable"])
async def test_async_template_state_actions(async_templates_service, action):
    response_expected_data = {"id": "NTL-1234", "status": "Active"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/notifications/templates/NTL-1234/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await getattr(async_templates_service, action)("NTL-1234")

        assert mock_route.call_count == 1
        assert result.to_dict() == response_expected_data


def test_variants_accessor(templates_service):
    result = templates_service.variants("NTL-1234")

    assert isinstance(result, TemplateVariantsService)
    assert result.http_client is templates_service.http_client
    assert result.endpoint_params == {"template_id": "NTL-1234"}
    assert result.build_path() == "/public/v1/notifications/templates/NTL-1234/variants"


def test_async_variants_accessor(async_templates_service):
    result = async_templates_service.variants("NTL-1234")

    assert isinstance(result, AsyncTemplateVariantsService)
    assert result.http_client is async_templates_service.http_client
    assert result.endpoint_params == {"template_id": "NTL-1234"}
    assert result.build_path() == "/public/v1/notifications/templates/NTL-1234/variants"

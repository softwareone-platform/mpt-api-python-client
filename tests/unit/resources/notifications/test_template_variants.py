import httpx
import pytest
import respx

from mpt_api_client.resources.notifications.template_variants import (
    AsyncTemplateVariantsService,
    TemplateVariantsService,
)

TEMPLATE_ID = "NTL-1234"
VARIANTS_PATH = f"/public/v1/notifications/templates/{TEMPLATE_ID}/variants"


@pytest.fixture
def template_variants_service(http_client):
    return TemplateVariantsService(
        http_client=http_client, endpoint_params={"template_id": TEMPLATE_ID}
    )


@pytest.fixture
def async_template_variants_service(async_http_client):
    return AsyncTemplateVariantsService(
        http_client=async_http_client, endpoint_params={"template_id": TEMPLATE_ID}
    )


@pytest.fixture
def template_variant_data():
    return {
        "id": "NTV-1234",
        "body": "Hello",
        "default": True,
        "languageCode": "en-US",
        "subject": "Order confirmed",
        "status": "Active",
        "template": {"id": TEMPLATE_ID, "name": "Order confirmation"},
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


def test_endpoint_contains_template_id(template_variants_service):
    result = template_variants_service.build_path()

    assert result == VARIANTS_PATH


def test_async_endpoint_contains_template_id(async_template_variants_service):
    result = async_template_variants_service.build_path()

    assert result == VARIANTS_PATH


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "activate", "disable", "iterate", "fetch_page"],
)
def test_mixins_present(template_variants_service, method):
    result = hasattr(template_variants_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "activate", "disable", "iterate", "fetch_page"],
)
def test_async_mixins_present(async_template_variants_service, method):
    result = hasattr(async_template_variants_service, method)

    assert result is True


def test_get_template_variant(template_variants_service, template_variant_data):
    with respx.mock:
        mock_route = respx.get(f"https://api.example.com{VARIANTS_PATH}/NTV-1234").mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "application/json"},
                json=template_variant_data,
            )
        )

        result = template_variants_service.get("NTV-1234")

        assert mock_route.call_count == 1
        assert result.to_dict() == template_variant_data
        assert result.language_code == "en-US"
        assert result.template.id == TEMPLATE_ID


@pytest.mark.parametrize("action", ["activate", "disable"])
def test_template_variant_state_actions(template_variants_service, action):
    response_expected_data = {"id": "NTV-1234", "status": "Active"}
    with respx.mock:
        mock_route = respx.post(f"https://api.example.com{VARIANTS_PATH}/NTV-1234/{action}").mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = getattr(template_variants_service, action)("NTV-1234")

        assert mock_route.call_count == 1
        assert result.to_dict() == response_expected_data


@pytest.mark.parametrize("action", ["activate", "disable"])
async def test_async_template_variant_state_actions(async_template_variants_service, action):
    response_expected_data = {"id": "NTV-1234", "status": "Active"}
    with respx.mock:
        mock_route = respx.post(f"https://api.example.com{VARIANTS_PATH}/NTV-1234/{action}").mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await getattr(async_template_variants_service, action)("NTV-1234")

        assert mock_route.call_count == 1
        assert result.to_dict() == response_expected_data

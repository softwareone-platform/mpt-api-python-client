import httpx
import pytest
import respx

from mpt_api_client.resources.helpdesk.forms import AsyncFormsService, Form, FormsService


@pytest.fixture
def forms_service(http_client):
    return FormsService(http_client=http_client)


@pytest.fixture
def async_forms_service(async_http_client):
    return AsyncFormsService(http_client=async_http_client)


def test_endpoint(forms_service):
    result = forms_service.path == "/public/v1/helpdesk/forms"

    assert result is True


def test_async_endpoint(async_forms_service):
    result = async_forms_service.path == "/public/v1/helpdesk/forms"

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "fetch_page", "iterate", "publish", "unpublish"],
)
def test_methods_present(forms_service, method):
    result = hasattr(forms_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "fetch_page", "iterate", "publish", "unpublish"],
)
def test_async_methods_present(async_forms_service, method):
    result = hasattr(async_forms_service, method)

    assert result is True


@pytest.mark.parametrize("action", ["publish", "unpublish"])
def test_custom_resource_actions(forms_service, action):
    response_expected_data = {"id": "FRM-1234-5678", "status": "Updated"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/helpdesk/forms/FRM-1234-5678/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = getattr(forms_service, action)("FRM-1234-5678")

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == b""
        assert result.to_dict() == response_expected_data
        assert isinstance(result, Form)


@pytest.mark.parametrize("action", ["publish", "unpublish"])
async def test_async_custom_resource_actions(async_forms_service, action):
    response_expected_data = {"id": "FRM-1234-5678", "status": "Updated"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/helpdesk/forms/FRM-1234-5678/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await getattr(async_forms_service, action)("FRM-1234-5678")

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == b""
        assert result.to_dict() == response_expected_data
        assert isinstance(result, Form)

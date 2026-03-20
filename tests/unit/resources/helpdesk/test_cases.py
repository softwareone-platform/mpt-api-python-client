import httpx
import pytest
import respx

from mpt_api_client.resources.helpdesk.cases import AsyncCasesService, Case, CasesService


def _request_content(action: str) -> bytes:
    if action == "query":
        return b'{"id":"CAS-1234-5678","queryPrompt":"Please provide more details"}'
    if action == "process":
        return b'{"id":"CAS-1234-5678","status":"Processing"}'
    return b'{"id":"CAS-1234-5678","status":"Completed"}'


@pytest.fixture
def cases_service(http_client):
    return CasesService(http_client=http_client)


@pytest.fixture
def async_cases_service(async_http_client):
    return AsyncCasesService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "fetch_page", "query", "process", "complete"],
)
def test_methods_present(cases_service, method):
    result = hasattr(cases_service, method)

    assert result is True


def test_delete_not_present(cases_service):
    result = hasattr(cases_service, "delete")

    assert result is False


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "fetch_page", "query", "process", "complete"],
)
def test_async_methods_present(async_cases_service, method):
    result = hasattr(async_cases_service, method)

    assert result is True


def test_async_delete_not_present(async_cases_service):
    result = hasattr(async_cases_service, "delete")

    assert result is False


@pytest.mark.parametrize(
    ("action", "input_data"),
    [
        ("query", {"id": "CAS-1234-5678", "queryPrompt": "Please provide more details"}),
        ("process", {"id": "CAS-1234-5678", "status": "Processing"}),
        ("complete", {"id": "CAS-1234-5678", "status": "Completed"}),
    ],
)
def test_custom_resource_actions(cases_service, action, input_data):
    request_expected_content = _request_content(action)
    response_expected_data = {"id": "CAS-1234-5678", "status": "Updated"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/helpdesk/cases/CAS-1234-5678/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = getattr(cases_service, action)("CAS-1234-5678", input_data)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, Case)


@pytest.mark.parametrize("action", ["query", "process", "complete"])
def test_custom_resource_actions_no_data(cases_service, action):
    response_expected_data = {"id": "CAS-1234-5678", "status": "Updated"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/helpdesk/cases/CAS-1234-5678/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = getattr(cases_service, action)("CAS-1234-5678")

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == b""
        assert result.to_dict() == response_expected_data
        assert isinstance(result, Case)


@pytest.mark.parametrize(
    ("action", "input_data"),
    [
        ("query", {"id": "CAS-1234-5678", "queryPrompt": "Please provide more details"}),
        ("process", {"id": "CAS-1234-5678", "status": "Processing"}),
        ("complete", {"id": "CAS-1234-5678", "status": "Completed"}),
    ],
)
async def test_async_custom_resource_actions(async_cases_service, action, input_data):
    request_expected_content = _request_content(action)
    response_expected_data = {"id": "CAS-1234-5678", "status": "Updated"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/helpdesk/cases/CAS-1234-5678/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await getattr(async_cases_service, action)("CAS-1234-5678", input_data)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, Case)


@pytest.mark.parametrize("action", ["query", "process", "complete"])
async def test_async_custom_resource_actions_no_data(async_cases_service, action):
    response_expected_data = {"id": "CAS-1234-5678", "status": "Updated"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/helpdesk/cases/CAS-1234-5678/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await getattr(async_cases_service, action)("CAS-1234-5678")

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == b""
        assert result.to_dict() == response_expected_data
        assert isinstance(result, Case)

import httpx
import pytest
import respx

from mpt_api_client.resources.helpdesk.queues import AsyncQueuesService, Queue, QueuesService


def _request_content(action: str) -> bytes:
    if action == "activate":
        return b'{"id":"HQU-1234-5678","status":"Active"}'
    return b'{"id":"HQU-1234-5678","status":"Disabled"}'


@pytest.fixture
def queues_service(http_client):
    return QueuesService(http_client=http_client)


@pytest.fixture
def async_queues_service(async_http_client):
    return AsyncQueuesService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "fetch_page", "iterate", "activate", "disable"],
)
def test_methods_present(queues_service, method):
    result = hasattr(queues_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "fetch_page", "iterate", "activate", "disable"],
)
def test_async_methods_present(async_queues_service, method):
    result = hasattr(async_queues_service, method)

    assert result is True


@pytest.mark.parametrize("action", ["activate", "disable"])
def test_custom_resource_actions(queues_service, action):
    response_expected_data = {"id": "HQU-1234-5678", "status": "Updated"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/helpdesk/queues/HQU-1234-5678/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = getattr(queues_service, action)("HQU-1234-5678")

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == b""
        assert result.to_dict() == response_expected_data
        assert isinstance(result, Queue)


@pytest.mark.parametrize("action", ["activate", "disable"])
async def test_async_custom_resource_actions(async_queues_service, action):
    response_expected_data = {"id": "HQU-1234-5678", "status": "Updated"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/helpdesk/queues/HQU-1234-5678/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await getattr(async_queues_service, action)("HQU-1234-5678")

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == b""
        assert result.to_dict() == response_expected_data
        assert isinstance(result, Queue)

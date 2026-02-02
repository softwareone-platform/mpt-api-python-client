import httpx
import pytest
import respx

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.resources.accounts.mixins.invitable_mixin import (
    AsyncInvitableMixin,
    InvitableMixin,
)
from tests.unit.conftest import DummyModel


class DummyInvitableService(
    InvitableMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/dummy/invitable/"
    _model_class = DummyModel
    _collection_key = "data"


class DummyAsyncInvitableService(
    AsyncInvitableMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/dummy/invitable/"
    _model_class = DummyModel
    _collection_key = "data"


@pytest.fixture
def invitable_service(http_client):
    return DummyInvitableService(http_client=http_client)


@pytest.fixture
def async_invitable_service(async_http_client):
    return DummyAsyncInvitableService(http_client=async_http_client)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("accept_invite", {"id": "OBJ-0000-0001", "status": "update"}),
        ("resend_invite", {"id": "OBJ-0000-0001", "status": "update"}),
        ("send_new_invite", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
def test_invitable_resource_actions(invitable_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    endpoint_action = action.replace("_", "-")
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/invitable/OBJ-0000-0001/{endpoint_action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = getattr(invitable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("accept_invite", None),
        ("resend_invite", None),
        ("send_new_invite", None),
    ],
)
def test_invitable_resource_actions_no_data(invitable_service, action, input_status):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    endpoint_action = action.replace("_", "-")
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/invitable/OBJ-0000-0001/{endpoint_action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = getattr(invitable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("accept_invite", {"id": "OBJ-0000-0001", "status": "update"}),
        ("resend_invite", {"id": "OBJ-0000-0001", "status": "update"}),
        ("send_new_invite", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
async def test_async_invitable_resource_actions(async_invitable_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    endpoint_action = action.replace("_", "-")
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/invitable/OBJ-0000-0001/{endpoint_action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await getattr(async_invitable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("accept_invite", None),
        ("resend_invite", None),
        ("send_new_invite", None),
    ],
)
async def test_async_invitable_resource_actions_no_data(
    async_invitable_service, action, input_status
):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    endpoint_action = action.replace("_", "-")
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/invitable/OBJ-0000-0001/{endpoint_action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await getattr(async_invitable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)

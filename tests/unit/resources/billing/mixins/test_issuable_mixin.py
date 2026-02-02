import httpx
import pytest
import respx

from mpt_api_client.http.async_service import AsyncService
from mpt_api_client.http.service import Service
from mpt_api_client.resources.billing.mixins.issuable_mixin import (
    AsyncIssuableMixin,
    IssuableMixin,
)
from tests.unit.conftest import DummyModel


class DummyIssuableService(
    IssuableMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/dummy/issuable/"
    _model_class = DummyModel
    _collection_key = "data"


class DummyAsyncIssuableService(
    AsyncIssuableMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/dummy/issuable/"
    _model_class = DummyModel
    _collection_key = "data"


@pytest.fixture
def issuable_service(http_client):
    return DummyIssuableService(http_client=http_client)


@pytest.fixture
def async_issuable_service(async_http_client):
    return DummyAsyncIssuableService(http_client=async_http_client)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("issue", {"id": "OBJ-0000-0001", "status": "update"}),
        ("cancel", {"id": "OBJ-0000-0001", "status": "update"}),
        ("error", {"id": "OBJ-0000-0001", "status": "update"}),
        ("pending", {"id": "OBJ-0000-0001", "status": "update"}),
        ("queue", {"id": "OBJ-0000-0001", "status": "update"}),
        ("retry", {"id": "OBJ-0000-0001", "status": "update"}),
        ("recalculate", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
def test_issuable_resource_actions(issuable_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/issuable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = getattr(issuable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("issue", None),
        ("cancel", None),
        ("error", None),
        ("pending", None),
        ("queue", None),
        ("retry", None),
        ("recalculate", None),
    ],
)
def test_issuable_resource_actions_no_data(issuable_service, action, input_status):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/issuable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = getattr(issuable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("issue", {"id": "OBJ-0000-0001", "status": "update"}),
        ("cancel", {"id": "OBJ-0000-0001", "status": "update"}),
        ("error", {"id": "OBJ-0000-0001", "status": "update"}),
        ("pending", {"id": "OBJ-0000-0001", "status": "update"}),
        ("queue", {"id": "OBJ-0000-0001", "status": "update"}),
        ("retry", {"id": "OBJ-0000-0001", "status": "update"}),
        ("recalculate", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
async def test_async_issuable_resource_actions(async_issuable_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/issuable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await getattr(async_issuable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("issue", None),
        ("cancel", None),
        ("error", None),
        ("pending", None),
        ("queue", None),
        ("retry", None),
        ("recalculate", None),
    ],
)
async def test_async_issuable_resource_actions_no_data(
    async_issuable_service, action, input_status
):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/issuable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await getattr(async_issuable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)

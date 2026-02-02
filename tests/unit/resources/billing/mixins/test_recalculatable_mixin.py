import httpx
import pytest
import respx

from mpt_api_client.http.async_service import AsyncService
from mpt_api_client.http.service import Service
from mpt_api_client.resources.billing.mixins.recalculatable_mixin import (
    AsyncRecalculatableMixin,
    RecalculatableMixin,
)
from tests.unit.conftest import DummyModel


class DummyRecalculatableService(
    RecalculatableMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/dummy/recalculatable/"
    _model_class = DummyModel
    _collection_key = "data"


class DummyAsyncRecalculatableService(
    AsyncRecalculatableMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/dummy/recalculatable/"
    _model_class = DummyModel
    _collection_key = "data"


@pytest.fixture
def recalculatable_service(http_client):
    return DummyRecalculatableService(http_client=http_client)


@pytest.fixture
def async_recalculatable_service(async_http_client):
    return DummyAsyncRecalculatableService(http_client=async_http_client)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("recalculate", {"id": "OBJ-0000-0001", "status": "update"}),
        ("accept", {"id": "OBJ-0000-0001", "status": "update"}),
        ("queue", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
def test_recalculate_resource_actions(recalculatable_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/recalculatable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = getattr(recalculatable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [("recalculate", None), ("accept", None), ("queue", None)],
)
def test_actions_no_data(recalculatable_service, action, input_status):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/recalculatable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = getattr(recalculatable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("recalculate", {"id": "OBJ-0000-0001", "status": "update"}),
        ("accept", {"id": "OBJ-0000-0001", "status": "update"}),
        ("queue", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
async def test_async_recalculate_resource_actions(
    async_recalculatable_service, action, input_status
):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/recalculatable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await getattr(async_recalculatable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [("recalculate", None), ("accept", None), ("queue", None)],
)
async def test_async_actions_no_data(async_recalculatable_service, action, input_status):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/recalculatable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await getattr(async_recalculatable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)

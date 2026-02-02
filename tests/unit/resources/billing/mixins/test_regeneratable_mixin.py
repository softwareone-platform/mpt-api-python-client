import httpx
import pytest
import respx

from mpt_api_client.http.async_service import AsyncService
from mpt_api_client.http.service import Service
from mpt_api_client.resources.billing.mixins.regeneratable_mixin import (
    AsyncRegeneratableMixin,
    RegeneratableMixin,
)
from tests.unit.conftest import DummyModel


class DummyRegeneratableService(
    RegeneratableMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/dummy/regeneratable/"
    _model_class = DummyModel
    _collection_key = "data"


class DummyAsyncRegeneratableService(
    AsyncRegeneratableMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/dummy/regeneratable/"
    _model_class = DummyModel
    _collection_key = "data"


@pytest.fixture
def regeneratable_service(http_client):
    return DummyRegeneratableService(http_client=http_client)


@pytest.fixture
def async_regeneratable_service(async_http_client):
    return DummyAsyncRegeneratableService(http_client=async_http_client)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("regenerate", {"id": "OBJ-0000-0001", "status": "update"}),
        ("submit", {"id": "OBJ-0000-0001", "status": "update"}),
        ("enquiry", {"id": "OBJ-0000-0001", "status": "update"}),
        ("accept", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
def test_custom_resource_actions(regeneratable_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/regeneratable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = getattr(regeneratable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("regenerate", None),
        ("submit", None),
        ("enquiry", None),
        ("accept", None),
    ],
)
def test_custom_resource_actions_no_data(regeneratable_service, action, input_status):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/regeneratable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = getattr(regeneratable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("regenerate", {"id": "OBJ-0000-0001", "status": "update"}),
        ("submit", {"id": "OBJ-0000-0001", "status": "update"}),
        ("enquiry", {"id": "OBJ-0000-0001", "status": "update"}),
        ("accept", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
async def test_async_custom_resource_actions(async_regeneratable_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/regeneratable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await getattr(async_regeneratable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("regenerate", None),
        ("submit", None),
        ("enquiry", None),
        ("accept", None),
    ],
)
async def test_async_custom_resource_actions_no_data(
    async_regeneratable_service, action, input_status
):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/regeneratable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await getattr(async_regeneratable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)

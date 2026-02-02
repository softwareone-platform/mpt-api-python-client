import httpx
import pytest
import respx

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.resources.accounts.mixins.validate_mixin import (
    AsyncValidateMixin,
    ValidateMixin,
)
from tests.unit.conftest import DummyModel


class DummyValidateService(
    ValidateMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/dummy/validate/"
    _model_class = DummyModel
    _collection_key = "data"


class DummyAsyncValidateService(
    AsyncValidateMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/dummy/validate/"
    _model_class = DummyModel
    _collection_key = "data"


@pytest.fixture
def validate_service(http_client):
    return DummyValidateService(http_client=http_client)


@pytest.fixture
def async_validate_service(async_http_client):
    return DummyAsyncValidateService(http_client=async_http_client)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("validate", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
def test_validate_resource_actions(validate_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/validate/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = getattr(validate_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("validate", None),
    ],
)
def test_validate_resource_actions_no_data(validate_service, action, input_status):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/validate/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = getattr(validate_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("validate", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
async def test_async_validate_resource_actions(async_validate_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/validate/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await getattr(async_validate_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("validate", None),
    ],
)
async def test_async_validate_resource_actions_no_data(
    async_validate_service, action, input_status
):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/validate/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await getattr(async_validate_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)

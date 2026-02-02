import httpx
import pytest
import respx

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import AsyncDisableMixin, DisableMixin
from tests.unit.conftest import DummyModel


class DisableService(
    DisableMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/dummy/enablable/"
    _model_class = DummyModel


class AsyncDisableService(
    AsyncDisableMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/dummy/enablable/"
    _model_class = DummyModel


@pytest.fixture
def disablable_service(http_client) -> DisableService:
    return DisableService(http_client=http_client)


@pytest.fixture
def async_disablable_service(async_http_client) -> AsyncDisableService:
    return AsyncDisableService(http_client=async_http_client)


@pytest.mark.parametrize(
    ("input_status"),
    [
        ({"id": "OBJ-0000-0001", "status": "update"}),
        (None),
    ],
)
def test_disable_resource_actions(
    disablable_service: DisableService, input_status: dict | None
) -> None:
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}' if input_status else b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/dummy/enablable/OBJ-0000-0001/disable"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = disablable_service.disable("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


@pytest.mark.parametrize(
    ("input_status"),
    [
        ({"id": "OBJ-0000-0001", "status": "update"}),
        (None),
    ],
)
async def test_async_disable_resource_actions(
    async_disablable_service: AsyncDisableService, input_status: dict | None
) -> None:
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}' if input_status else b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/dummy/enablable/OBJ-0000-0001/disable"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await async_disablable_service.disable("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)

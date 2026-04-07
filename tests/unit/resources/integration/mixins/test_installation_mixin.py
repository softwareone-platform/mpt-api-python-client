import httpx
import pytest
import respx

from mpt_api_client.http.async_service import AsyncService
from mpt_api_client.http.service import Service
from mpt_api_client.resources.integration.mixins import (
    AsyncInstallationMixin,
    InstallationMixin,
)
from tests.unit.conftest import DummyModel


class DummyInstallationService(
    InstallationMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/integration/installations"
    _model_class = DummyModel
    _collection_key = "data"


class DummyAsyncInstallationService(
    AsyncInstallationMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/integration/installations"
    _model_class = DummyModel
    _collection_key = "data"


@pytest.fixture
def installation_service(http_client):
    return DummyInstallationService(http_client=http_client)


@pytest.fixture
def async_installation_service(async_http_client):
    return DummyAsyncInstallationService(http_client=async_http_client)


@pytest.mark.parametrize(
    "action",
    ["invite", "install", "uninstall", "expire"],
)
def test_post_actions(installation_service, action):
    installation_id = "INS-001"
    expected_response = {"id": installation_id, "status": "updated"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/integration/installations/{installation_id}/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=expected_response,
            )
        )

        result = getattr(installation_service, action)(installation_id)

        assert mock_route.call_count == 1
        assert mock_route.calls[0].request.method == "POST"
        assert result.to_dict() == expected_response
        assert isinstance(result, DummyModel)


@pytest.mark.parametrize(
    "action",
    ["invite", "install", "uninstall", "expire"],
)
async def test_async_post_actions(async_installation_service, action):
    installation_id = "INS-001"
    expected_response = {"id": installation_id, "status": "updated"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/integration/installations/{installation_id}/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=expected_response,
            )
        )

        result = await getattr(async_installation_service, action)(installation_id)

        assert mock_route.call_count == 1
        assert mock_route.calls[0].request.method == "POST"
        assert result.to_dict() == expected_response
        assert isinstance(result, DummyModel)

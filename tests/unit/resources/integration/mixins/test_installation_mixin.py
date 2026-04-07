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


def test_redeem(installation_service):
    installation_id = "INS-001"
    expected_response = {"id": installation_id, "status": "Installed"}
    payload = {"code": "ABC123", "modules": [{"id": "MOD-001"}]}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/integration/installations/{installation_id}/redeem"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=expected_response,
            )
        )

        result = installation_service.redeem(installation_id, payload)

        assert mock_route.call_count == 1
        assert mock_route.calls[0].request.method == "POST"
        assert (
            mock_route.calls[0].request.content == b'{"code":"ABC123","modules":[{"id":"MOD-001"}]}'
        )
        assert result.to_dict() == expected_response
        assert isinstance(result, DummyModel)


async def test_async_redeem(async_installation_service):
    installation_id = "INS-001"
    expected_response = {"id": installation_id, "status": "Installed"}
    payload = {"code": "ABC123", "modules": [{"id": "MOD-001"}]}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/integration/installations/{installation_id}/redeem"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=expected_response,
            )
        )

        result = await async_installation_service.redeem(installation_id, payload)

        assert mock_route.call_count == 1
        assert mock_route.calls[0].request.method == "POST"
        assert (
            mock_route.calls[0].request.content == b'{"code":"ABC123","modules":[{"id":"MOD-001"}]}'
        )
        assert result.to_dict() == expected_response
        assert isinstance(result, DummyModel)

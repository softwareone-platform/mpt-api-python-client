import httpx
import pytest
import respx

from mpt_api_client.resources.integration.installations_token import (
    AsyncInstallationsTokenService,
    InstallationsToken,
    InstallationsTokenService,
)
from tests.unit.conftest import API_URL

TOKEN_URL = f"{API_URL}/public/v1/integration/installations/-/token"


@pytest.fixture
def installations_token_service(http_client):
    return InstallationsTokenService(http_client=http_client)


@pytest.fixture
def async_installations_token_service(async_http_client):
    return AsyncInstallationsTokenService(http_client=async_http_client)


def test_token_endpoint(installations_token_service):
    endpoint = installations_token_service.path  # act

    assert endpoint == "/public/v1/integration/installations/-/token"


def test_token_posts_and_returns_model(installations_token_service):
    with respx.mock:
        mock_route = respx.post(TOKEN_URL).mock(
            return_value=httpx.Response(httpx.codes.CREATED, json={"token": "installation-token"})
        )

        result = installations_token_service.token()

    request = mock_route.calls[0].request
    assert isinstance(result, InstallationsToken)
    assert result.token == "installation-token"
    assert request.method == "POST"
    assert "account.id" not in request.url.params


def test_token_account_scoped(installations_token_service):
    with respx.mock:
        mock_route = respx.post(TOKEN_URL).mock(
            return_value=httpx.Response(httpx.codes.CREATED, json={"token": "account-token"})
        )

        result = installations_token_service.token("ACC-123")

    request = mock_route.calls[0].request
    assert result.token == "account-token"
    assert request.url.params["account.id"] == "ACC-123"


async def test_async_token_account_scoped(async_installations_token_service):
    with respx.mock:
        mock_route = respx.post(TOKEN_URL).mock(
            return_value=httpx.Response(httpx.codes.CREATED, json={"token": "account-token"})
        )

        result = await async_installations_token_service.token("ACC-123")

    request = mock_route.calls[0].request
    assert result.token == "account-token"
    assert request.url.params["account.id"] == "ACC-123"

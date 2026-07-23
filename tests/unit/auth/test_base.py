import httpx

from mpt_api_client.auth import BearerTokenAuthentication
from mpt_api_client.config import ClientConfig
from tests.unit.conftest import API_URL


def test_configure_returns_config_unchanged():
    authentication = BearerTokenAuthentication("my-token")
    config = ClientConfig(base_url=API_URL, timeout=30.0, retries=2)

    result = authentication.configure(config)  # act

    assert result == config


def test_bearer_token_sets_authorization_header():
    authentication = BearerTokenAuthentication("my-token")
    request = httpx.Request("GET", f"{API_URL}/")

    sent = next(authentication.auth_flow(request))  # act

    assert sent.headers["Authorization"] == "Bearer my-token"

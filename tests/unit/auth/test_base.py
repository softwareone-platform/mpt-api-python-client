import httpx
import pytest

from mpt_api_client.auth import BearerTokenAuthentication, EnvTokenAuthentication
from mpt_api_client.exceptions import MPTError
from tests.unit.conftest import API_URL

ENV_API_TOKEN = "MPT_API_TOKEN"


def test_bearer_token_sets_authorization_header():
    authentication = BearerTokenAuthentication("my-token")
    request = httpx.Request("GET", f"{API_URL}/")

    sent = next(authentication.auth_flow(request))  # act

    assert sent.headers["Authorization"] == "Bearer my-token"


def test_env_token_reads_token_from_env(monkeypatch):
    monkeypatch.setenv(ENV_API_TOKEN, "env-token")
    request = httpx.Request("GET", f"{API_URL}/")

    authentication = EnvTokenAuthentication()  # act

    sent = next(authentication.auth_flow(request))
    assert sent.headers["Authorization"] == "Bearer env-token"


def test_env_token_reads_custom_env_var(monkeypatch):
    monkeypatch.setenv("MPT_API_TOKEN_VENDOR", "vendor-token")
    request = httpx.Request("GET", f"{API_URL}/")

    authentication = EnvTokenAuthentication("MPT_API_TOKEN_VENDOR")  # act

    sent = next(authentication.auth_flow(request))
    assert sent.headers["Authorization"] == "Bearer vendor-token"


def test_env_token_missing_env_var_raises(monkeypatch):
    monkeypatch.delenv(ENV_API_TOKEN, raising=False)

    with pytest.raises(MPTError, match=ENV_API_TOKEN):  # act
        EnvTokenAuthentication()

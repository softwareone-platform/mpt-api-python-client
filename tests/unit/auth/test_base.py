import httpx

from mpt_api_client.auth import BearerTokenAuthentication
from tests.unit.conftest import API_URL


def test_bearer_token_sets_authorization_header():
    authentication = BearerTokenAuthentication("my-token")
    request = httpx.Request("GET", f"{API_URL}/")

    sent = next(authentication.auth_flow(request))  # act

    assert sent.headers["Authorization"] == "Bearer my-token"

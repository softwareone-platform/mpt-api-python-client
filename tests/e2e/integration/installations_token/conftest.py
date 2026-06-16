import pytest

from mpt_api_client import AsyncMPTClient, BearerTokenAuthentication, MPTClient


@pytest.fixture
def installations_token_service(extension_secret, base_url, api_timeout):
    client = MPTClient.from_config(
        authentication=BearerTokenAuthentication(extension_secret),
        base_url=base_url,
        timeout=api_timeout,
    )
    return client.integration.installations_token()


@pytest.fixture
def async_installations_token_service(extension_secret, base_url, api_timeout):
    client = AsyncMPTClient.from_config(
        authentication=BearerTokenAuthentication(extension_secret),
        base_url=base_url,
        timeout=api_timeout,
    )
    return client.integration.installations_token()

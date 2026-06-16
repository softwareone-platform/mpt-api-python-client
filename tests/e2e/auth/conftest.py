import pytest

from mpt_api_client import AsyncMPTClient, ExtensionFrameworkAuthentication, MPTClient


@pytest.fixture
def mpt_extension_framework(extension_secret, installation_account_id, base_url, api_timeout):
    return MPTClient.from_config(
        authentication=ExtensionFrameworkAuthentication(
            secret=extension_secret, account_id=installation_account_id
        ),
        base_url=base_url,
        timeout=api_timeout,
    )


@pytest.fixture
def async_mpt_extension_framework(extension_secret, installation_account_id, base_url, api_timeout):
    return AsyncMPTClient.from_config(
        authentication=ExtensionFrameworkAuthentication(
            secret=extension_secret, account_id=installation_account_id
        ),
        base_url=base_url,
        timeout=api_timeout,
    )

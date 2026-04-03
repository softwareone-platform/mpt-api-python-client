import pytest

from mpt_api_client.resources.integration.integration import (
    AsyncIntegration,
    Integration,
)


@pytest.fixture
def integration(http_client):
    return Integration(http_client=http_client)


@pytest.fixture
def async_integration(async_http_client):
    return AsyncIntegration(http_client=async_http_client)

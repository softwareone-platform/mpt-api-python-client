import pytest

from mpt_api_client.resources.integration.extensions import (
    AsyncExtensionsService,
    ExtensionsService,
)
from mpt_api_client.resources.integration.installations import (
    AsyncInstallationsService,
    InstallationsService,
)
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


def test_integration_initialization(http_client):
    result = Integration(http_client=http_client)

    assert result.http_client is http_client
    assert isinstance(result, Integration)


def test_async_integration_initialization(async_http_client):
    result = AsyncIntegration(http_client=async_http_client)

    assert result.http_client is async_http_client
    assert isinstance(result, AsyncIntegration)


@pytest.mark.parametrize(
    ("property_name", "expected_service_class"),
    [
        ("extensions", ExtensionsService),
        ("installations", InstallationsService),
    ],
)
def test_integration_properties(integration, property_name, expected_service_class):
    result = getattr(integration, property_name)

    assert isinstance(result, expected_service_class)
    assert result.http_client is integration.http_client


@pytest.mark.parametrize(
    ("property_name", "expected_service_class"),
    [
        ("extensions", AsyncExtensionsService),
        ("installations", AsyncInstallationsService),
    ],
)
def test_async_integration_properties(async_integration, property_name, expected_service_class):
    result = getattr(async_integration, property_name)

    assert isinstance(result, expected_service_class)
    assert result.http_client is async_integration.http_client

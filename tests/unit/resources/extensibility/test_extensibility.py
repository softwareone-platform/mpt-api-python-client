import pytest

from mpt_api_client.resources.extensibility.extensibility import (
    AsyncExtensibility,
    Extensibility,
)
from mpt_api_client.resources.extensibility.extensions import (
    AsyncExtensionsService,
    ExtensionsService,
)


@pytest.fixture
def extensibility(http_client):
    return Extensibility(http_client=http_client)


@pytest.fixture
def async_extensibility(async_http_client):
    return AsyncExtensibility(http_client=async_http_client)


def test_extensibility_initialization(http_client):
    result = Extensibility(http_client=http_client)

    assert result.http_client is http_client
    assert isinstance(result, Extensibility)


def test_async_extensibility_initialization(async_http_client):
    result = AsyncExtensibility(http_client=async_http_client)

    assert result.http_client is async_http_client
    assert isinstance(result, AsyncExtensibility)


@pytest.mark.parametrize(
    ("property_name", "expected_service_class"),
    [
        ("extensions", ExtensionsService),
    ],
)
def test_extensibility_properties(extensibility, property_name, expected_service_class):
    result = getattr(extensibility, property_name)

    assert isinstance(result, expected_service_class)
    assert result.http_client is extensibility.http_client


@pytest.mark.parametrize(
    ("property_name", "expected_service_class"),
    [
        ("extensions", AsyncExtensionsService),
    ],
)
def test_async_extensibility_properties(async_extensibility, property_name, expected_service_class):
    result = getattr(async_extensibility, property_name)

    assert isinstance(result, expected_service_class)
    assert result.http_client is async_extensibility.http_client

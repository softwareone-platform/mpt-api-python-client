import pytest

from mpt_api_client.resources.spotlight.objects import (
    AsyncSpotlightObjectsService,
    SpotlightObjectsService,
)
from mpt_api_client.resources.spotlight.queries import (
    AsyncSpotlightQueriesService,
    SpotlightQueriesService,
)
from mpt_api_client.resources.spotlight.spotlight import AsyncSpotlight, Spotlight


@pytest.fixture
def spotlight(http_client):
    return Spotlight(http_client=http_client)


@pytest.fixture
def async_spotlight(async_http_client):
    return AsyncSpotlight(http_client=async_http_client)


@pytest.mark.parametrize(
    ("property_name", "expected_service_class"),
    [
        ("objects", SpotlightObjectsService),
        ("queries", SpotlightQueriesService),
    ],
)
def test_spotlight_properties(spotlight, property_name, expected_service_class):
    result = getattr(spotlight, property_name)

    assert isinstance(result, expected_service_class)
    assert result.http_client is spotlight.http_client


@pytest.mark.parametrize(
    ("property_name", "expected_service_class"),
    [
        ("objects", AsyncSpotlightObjectsService),
        ("queries", AsyncSpotlightQueriesService),
    ],
)
def test_async_spotlight_properties(async_spotlight, property_name, expected_service_class):
    result = getattr(async_spotlight, property_name)

    assert isinstance(result, expected_service_class)
    assert result.http_client is async_spotlight.http_client


def test_spotlight_initialization(http_client):
    result = Spotlight(http_client=http_client)

    assert result.http_client is http_client
    assert isinstance(result, Spotlight)


def test_async_spotlight_initialization(async_http_client):
    result = AsyncSpotlight(http_client=async_http_client)

    assert result.http_client is async_http_client
    assert isinstance(result, AsyncSpotlight)

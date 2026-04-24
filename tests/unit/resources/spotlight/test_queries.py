import pytest

from mpt_api_client.resources.spotlight.queries import (
    AsyncSpotlightQueriesService,
    SpotlightQueriesService,
    SpotlightQuery,
)


@pytest.fixture
def spotlight_query_service(http_client):
    return SpotlightQueriesService(http_client=http_client)


@pytest.fixture
def async_spotlight_query_service(async_http_client):
    return AsyncSpotlightQueriesService(http_client=async_http_client)


@pytest.fixture
def spotlight_query_data():
    return {
        "id": "SPQ-123",
        "name": "Spotlight Query",
        "template": "Template String",
        "invalidationInterval": "24h",
        "invalidateOnDateChange": True,
        "filter": "Filter String",
        "scope": "Scope String",
    }


@pytest.mark.parametrize(
    "method",
    ["get", "iterate"],
)
def test_mixins_present(spotlight_query_service, method):
    result = hasattr(spotlight_query_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "iterate"],
)
def test_mixins_present_async(async_spotlight_query_service, method):
    result = hasattr(async_spotlight_query_service, method)

    assert result is True


def test_queries_primitive_fields(spotlight_query_data):
    result = SpotlightQuery(spotlight_query_data)

    assert result.to_dict() == spotlight_query_data


def test_queries_optional_fields():  # noqa: WPS218
    result = SpotlightQuery({"id": "SPQ-123"})

    assert not hasattr(result, "name")
    assert not hasattr(result, "template")
    assert not hasattr(result, "invalidation_interval")
    assert not hasattr(result, "invalidate_on_date_change")
    assert not hasattr(result, "filter")
    assert not hasattr(result, "scope")

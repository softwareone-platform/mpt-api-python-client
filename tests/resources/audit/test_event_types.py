import pytest

from mpt_api_client.resources.audit.event_types import AsyncEventTypesService, EventTypesService


@pytest.fixture
def event_types_service(http_client):
    return EventTypesService(http_client=http_client)


@pytest.fixture
def async_event_types_service(async_http_client):
    return AsyncEventTypesService(http_client=async_http_client)


@pytest.mark.parametrize("method", ["get", "update"])
def test_mixins_present(event_types_service, method):
    assert hasattr(event_types_service, method)


@pytest.mark.parametrize("method", ["get", "update"])
def test_async_mixins_present(async_event_types_service, method):
    assert hasattr(async_event_types_service, method)

import pytest

from mpt_api_client.resources.notifications.subscribers import (
    AsyncSubscribersService,
    SubscribersService,
)


@pytest.fixture
def subscribers_service(http_client):
    return SubscribersService(http_client=http_client)


@pytest.fixture
def async_subscribers_service(async_http_client):
    return AsyncSubscribersService(http_client=async_http_client)


@pytest.mark.parametrize("method", ["create", "update", "delete", "get", "iterate"])
def test_mixins_present(subscribers_service, method):
    result = hasattr(subscribers_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["create", "update", "delete", "get", "iterate"])
def test_async_mixins_present(async_subscribers_service, method):
    result = hasattr(async_subscribers_service, method)

    assert result is True

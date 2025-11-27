import pytest

from mpt_api_client.resources.notifications.messages import (
    AsyncMessagesService,
    MessagesService,
)


@pytest.fixture
def messages_service(http_client):
    return MessagesService(http_client=http_client)


@pytest.fixture
def async_messages_service(async_http_client):
    return AsyncMessagesService(http_client=async_http_client)


def test_messages_service_instance(messages_service):
    result = isinstance(messages_service, MessagesService)

    assert result is True


def test_async_messages_service_instance(async_messages_service):
    result = isinstance(async_messages_service, AsyncMessagesService)

    assert result is True


@pytest.mark.parametrize("method", ["get", "iterate"])
def test_sync_messages_service_methods(messages_service, method):
    result = hasattr(messages_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "iterate"])
def test_async_messages_service_methods(async_messages_service, method):
    result = hasattr(async_messages_service, method)

    assert result is True

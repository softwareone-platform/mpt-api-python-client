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
    assert isinstance(messages_service, MessagesService)


def test_async_messages_service_instance(async_messages_service):
    assert isinstance(async_messages_service, AsyncMessagesService)


@pytest.mark.parametrize("method", ["get", "iterate"])
def test_sync_messages_service_methods(messages_service, method):
    assert hasattr(messages_service, method)


@pytest.mark.parametrize("method", ["get", "iterate"])
def test_async_messages_service_methods(async_messages_service, method):
    assert hasattr(async_messages_service, method)

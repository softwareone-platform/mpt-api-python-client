import pytest

from mpt_api_client.resources.helpdesk.chat_messages import (
    AsyncChatMessagesService,
    ChatMessagesService,
)
from mpt_api_client.resources.helpdesk.chats import AsyncChatsService, ChatsService


@pytest.fixture
def chats_service(http_client):
    return ChatsService(http_client=http_client)


@pytest.fixture
def async_chats_service(async_http_client):
    return AsyncChatsService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "iterate"],
)
def test_mixins_present(chats_service, method):
    result = hasattr(chats_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "iterate"],
)
def test_async_mixins_present(async_chats_service, method):
    result = hasattr(async_chats_service, method)

    assert result is True


def test_messages_service(chats_service):
    result = chats_service.messages("CHT-0000-0000-0001")

    assert isinstance(result, ChatMessagesService)
    assert result.endpoint_params == {"chat_id": "CHT-0000-0000-0001"}


def test_async_messages_service(async_chats_service):
    result = async_chats_service.messages("CHT-0000-0000-0001")

    assert isinstance(result, AsyncChatMessagesService)
    assert result.endpoint_params == {"chat_id": "CHT-0000-0000-0001"}

import pytest

from mpt_api_client.resources.helpdesk.chat_messages import (
    AsyncChatMessagesService,
    ChatMessagesService,
)


@pytest.fixture
def chat_messages_service(http_client) -> ChatMessagesService:
    return ChatMessagesService(
        http_client=http_client, endpoint_params={"chat_id": "CHT-0000-0000-0001"}
    )


@pytest.fixture
def async_chat_messages_service(async_http_client) -> AsyncChatMessagesService:
    return AsyncChatMessagesService(
        http_client=async_http_client, endpoint_params={"chat_id": "CHT-0000-0000-0001"}
    )


def test_endpoint(chat_messages_service) -> None:
    result = chat_messages_service.path == "/public/v1/helpdesk/chats/CHT-0000-0000-0001/messages"

    assert result is True


def test_async_endpoint(async_chat_messages_service) -> None:
    result = (
        async_chat_messages_service.path == "/public/v1/helpdesk/chats/CHT-0000-0000-0001/messages"
    )

    assert result is True


@pytest.mark.parametrize("method", ["create", "update", "delete", "iterate"])
def test_methods_present(chat_messages_service, method: str) -> None:
    result = hasattr(chat_messages_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["create", "update", "delete", "iterate"])
def test_async_methods_present(async_chat_messages_service, method: str) -> None:
    result = hasattr(async_chat_messages_service, method)

    assert result is True

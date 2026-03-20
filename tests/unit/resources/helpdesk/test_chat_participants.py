import pytest

from mpt_api_client.resources.helpdesk.chat_participants import (
    AsyncChatParticipantsService,
    ChatParticipantsService,
)


@pytest.fixture
def chat_participants_service(http_client) -> ChatParticipantsService:
    return ChatParticipantsService(
        http_client=http_client, endpoint_params={"chat_id": "CHT-0000-0000-0001"}
    )


@pytest.fixture
def async_chat_participants_service(async_http_client) -> AsyncChatParticipantsService:
    return AsyncChatParticipantsService(
        http_client=async_http_client, endpoint_params={"chat_id": "CHT-0000-0000-0001"}
    )


def test_endpoint(chat_participants_service) -> None:
    result = (
        chat_participants_service.path
        == "/public/v1/helpdesk/chats/CHT-0000-0000-0001/participants"
    )

    assert result is True


def test_async_endpoint(async_chat_participants_service) -> None:
    result = (
        async_chat_participants_service.path
        == "/public/v1/helpdesk/chats/CHT-0000-0000-0001/participants"
    )

    assert result is True


@pytest.mark.parametrize("method", ["create", "update", "delete", "iterate"])
def test_methods_present(chat_participants_service, method: str) -> None:
    result = hasattr(chat_participants_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["create", "update", "delete", "iterate"])
def test_async_methods_present(async_chat_participants_service, method: str) -> None:
    result = hasattr(async_chat_participants_service, method)

    assert result is True

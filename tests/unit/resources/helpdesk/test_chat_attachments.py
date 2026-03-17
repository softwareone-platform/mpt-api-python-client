import pytest

from mpt_api_client.resources.helpdesk.chat_attachments import (
    AsyncChatAttachmentsService,
    ChatAttachmentsService,
)


@pytest.fixture
def chat_attachments_service(http_client) -> ChatAttachmentsService:
    return ChatAttachmentsService(
        http_client=http_client, endpoint_params={"chat_id": "CHT-0000-0000-0001"}
    )


@pytest.fixture
def async_chat_attachments_service(async_http_client) -> AsyncChatAttachmentsService:
    return AsyncChatAttachmentsService(
        http_client=async_http_client, endpoint_params={"chat_id": "CHT-0000-0000-0001"}
    )


def test_endpoint(chat_attachments_service) -> None:
    expected_path = "/public/v1/helpdesk/chats/CHT-0000-0000-0001/attachments"

    result = chat_attachments_service.path == expected_path

    assert result is True


def test_async_endpoint(async_chat_attachments_service) -> None:
    result = (
        async_chat_attachments_service.path
        == "/public/v1/helpdesk/chats/CHT-0000-0000-0001/attachments"
    )

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate", "download"])
def test_methods_present(chat_attachments_service, method: str) -> None:
    result = hasattr(chat_attachments_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate", "download"])
def test_async_methods_present(async_chat_attachments_service, method: str) -> None:
    result = hasattr(async_chat_attachments_service, method)

    assert result is True

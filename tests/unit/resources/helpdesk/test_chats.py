import pytest

from mpt_api_client.resources.helpdesk.chat_links import (
    AsyncChatLinksService,
    ChatLinksService,
)
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


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("messages", ChatMessagesService),
        ("links", ChatLinksService),
    ],
)
def test_property_services(chats_service, service_method, expected_service_class):
    result = getattr(chats_service, service_method)("CHT-0000-0000-0001")

    assert isinstance(result, expected_service_class)
    assert result.endpoint_params == {"chat_id": "CHT-0000-0000-0001"}


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("messages", AsyncChatMessagesService),
        ("links", AsyncChatLinksService),
    ],
)
def test_async_property_services(async_chats_service, service_method, expected_service_class):
    result = getattr(async_chats_service, service_method)("CHT-0000-0000-0001")

    assert isinstance(result, expected_service_class)
    assert result.endpoint_params == {"chat_id": "CHT-0000-0000-0001"}

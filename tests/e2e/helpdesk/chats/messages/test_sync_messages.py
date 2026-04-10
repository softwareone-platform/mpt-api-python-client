from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.helpdesk.chat_messages import ChatMessage

pytestmark = [pytest.mark.flaky]


def test_list_chat_messages(chat_messages_service):
    result = chat_messages_service.fetch_page(limit=1)

    assert len(result) > 0
    assert all(isinstance(message, ChatMessage) for message in result)


def test_create_chat_message(created_chat_message, chat_message_data):  # noqa: AAA01
    assert isinstance(created_chat_message, ChatMessage)
    assert created_chat_message.to_dict().get("content") == chat_message_data["content"]


def test_update_chat_message_visibility(chat_messages_service, created_chat_message):
    result = chat_messages_service.update(created_chat_message.id, {"visibility": "Public"})

    assert isinstance(result, ChatMessage)


def test_delete_chat_message(chat_messages_service, created_chat_message):
    result = created_chat_message

    chat_messages_service.delete(result.id)


def test_update_chat_message_not_found(chat_messages_service, invalid_chat_message_id):
    with pytest.raises(MPTAPIError) as error:
        chat_messages_service.update(invalid_chat_message_id, {"visibility": "Public"})

    assert error.value.status_code == HTTPStatus.NOT_FOUND


def test_delete_chat_message_not_found(chat_messages_service, invalid_chat_message_id):
    with pytest.raises(MPTAPIError) as error:
        chat_messages_service.delete(invalid_chat_message_id)

    assert error.value.status_code == HTTPStatus.NOT_FOUND

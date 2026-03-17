import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


def test_list_chat_messages(chat_messages_service):
    result = chat_messages_service.fetch_page(limit=1)

    assert len(result) > 0


def test_create_chat_message(created_chat_message, chat_message_data):  # noqa: AAA01
    assert created_chat_message.id is not None
    assert created_chat_message.to_dict().get("content") == chat_message_data["content"]


def test_update_chat_message_visibility(chat_messages_service, created_chat_message):
    result = chat_messages_service.update(created_chat_message.id, {"visibility": "Public"})

    assert result.id == created_chat_message.id


def test_delete_chat_message(chat_messages_service, created_chat_message):
    result = created_chat_message

    chat_messages_service.delete(result.id)


def test_update_chat_message_not_found(chat_messages_service, invalid_chat_message_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        chat_messages_service.update(invalid_chat_message_id, {"visibility": "Public"})


def test_delete_chat_message_not_found(chat_messages_service, invalid_chat_message_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        chat_messages_service.delete(invalid_chat_message_id)

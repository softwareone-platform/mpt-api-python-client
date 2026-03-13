import pytest

from mpt_api_client.exceptions import MPTAPIError


def test_get_chat(mpt_ops, chat_id):
    service = mpt_ops.helpdesk.chats

    result = service.get(chat_id)

    assert result.id == chat_id


def test_list_chats(mpt_ops):
    service = mpt_ops.helpdesk.chats

    result = service.fetch_page(limit=1)

    assert len(result) > 0


def test_update_chat(mpt_ops, chat_id, short_uuid):
    service = mpt_ops.helpdesk.chats
    new_description = f"e2e update {short_uuid}"

    result = service.update(chat_id, {"description": new_description})

    assert result.id == chat_id
    assert result.to_dict().get("description") == new_description


def test_not_found(mpt_ops, invalid_chat_id):
    service = mpt_ops.helpdesk.chats

    with pytest.raises(MPTAPIError):
        service.get(invalid_chat_id)

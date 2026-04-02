from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.helpdesk.chats import Chat

pytestmark = [pytest.mark.flaky]


def test_get_chat(mpt_ops, created_chat):
    service = mpt_ops.helpdesk.chats

    result = service.get(created_chat.id)

    assert result.id == created_chat.id


def test_list_chats(mpt_ops):
    service = mpt_ops.helpdesk.chats

    result = service.fetch_page(limit=1)

    assert len(result) > 0
    assert all(isinstance(chat, Chat) for chat in result)


def test_update_chat(mpt_ops, created_chat, short_uuid):
    service = mpt_ops.helpdesk.chats
    new_description = f"e2e update {short_uuid}"

    result = service.update(created_chat.id, {"description": new_description})

    assert result.id == created_chat.id
    assert result.to_dict().get("description") == new_description


def test_not_found(mpt_ops, invalid_chat_id):
    service = mpt_ops.helpdesk.chats

    with pytest.raises(MPTAPIError) as error:
        service.get(invalid_chat_id)

    assert error.value.status_code == HTTPStatus.NOT_FOUND

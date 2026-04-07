from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.helpdesk.chat_messages import ChatMessage

pytestmark = [pytest.mark.flaky]


async def test_list_chat_messages(async_chat_messages_service):
    result = await async_chat_messages_service.fetch_page(limit=1)

    assert len(result) > 0
    assert all(isinstance(message, ChatMessage) for message in result)


def test_create_chat_message(async_created_chat_message, chat_message_data):  # noqa: AAA01
    assert isinstance(async_created_chat_message, ChatMessage)
    assert async_created_chat_message.to_dict().get("content") == chat_message_data["content"]


async def test_update_chat_message_visibility(
    async_chat_messages_service, async_created_chat_message
):
    result = await async_chat_messages_service.update(
        async_created_chat_message.id,
        {"visibility": "Public"},
    )

    assert isinstance(result, ChatMessage)


async def test_delete_chat_message(async_chat_messages_service, async_created_chat_message):
    result = async_created_chat_message

    await async_chat_messages_service.delete(result.id)


@pytest.mark.skip(reason="Unskip after MPT-19964 completed")
async def test_update_chat_message_not_found(async_chat_messages_service, invalid_chat_message_id):
    with pytest.raises(MPTAPIError) as error:
        await async_chat_messages_service.update(
            invalid_chat_message_id,
            {"visibility": "Public"},
        )
    assert error.value.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.skip(reason="Unskip after MPT-19964 completed")
async def test_delete_chat_message_not_found(async_chat_messages_service, invalid_chat_message_id):
    with pytest.raises(MPTAPIError) as error:
        await async_chat_messages_service.delete(invalid_chat_message_id)
    assert error.value.status_code == HTTPStatus.NOT_FOUND

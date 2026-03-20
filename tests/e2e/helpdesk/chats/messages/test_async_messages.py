import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_list_chat_messages(async_chat_messages_service):
    result = await async_chat_messages_service.fetch_page(limit=1)

    assert len(result) > 0


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")  # noqa: AAA01
def test_create_chat_message(async_created_chat_message, chat_message_data):
    assert async_created_chat_message.id is not None
    assert async_created_chat_message.to_dict().get("content") == chat_message_data["content"]


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_update_chat_message_visibility(
    async_chat_messages_service, async_created_chat_message
):
    result = await async_chat_messages_service.update(
        async_created_chat_message.id,
        {"visibility": "Public"},
    )

    assert result.id == async_created_chat_message.id


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_delete_chat_message(async_chat_messages_service, async_created_chat_message):
    result = async_created_chat_message

    await async_chat_messages_service.delete(result.id)


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_update_chat_message_not_found(async_chat_messages_service, invalid_chat_message_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_chat_messages_service.update(
            invalid_chat_message_id,
            {"visibility": "Public"},
        )


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_delete_chat_message_not_found(async_chat_messages_service, invalid_chat_message_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_chat_messages_service.delete(invalid_chat_message_id)

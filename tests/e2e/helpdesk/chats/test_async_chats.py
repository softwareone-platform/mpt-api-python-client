import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_get_chat(async_mpt_ops, chat_id):
    service = async_mpt_ops.helpdesk.chats

    result = await service.get(chat_id)

    assert result.id == chat_id


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_list_chats(async_mpt_ops):
    service = async_mpt_ops.helpdesk.chats

    result = await service.fetch_page(limit=1)

    assert len(result) > 0


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_update_chat(async_mpt_ops, chat_id, short_uuid):
    service = async_mpt_ops.helpdesk.chats
    new_description = f"e2e update {short_uuid}"

    result = await service.update(chat_id, {"description": new_description})

    assert result.id == chat_id
    assert result.to_dict().get("description") == new_description


async def test_not_found(async_mpt_ops, invalid_chat_id):
    service = async_mpt_ops.helpdesk.chats

    with pytest.raises(MPTAPIError):
        await service.get(invalid_chat_id)

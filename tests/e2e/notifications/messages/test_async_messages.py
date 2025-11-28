import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


async def test_get_message(async_mpt_client, message_id):
    service = async_mpt_client.notifications.messages

    result = await service.get(message_id)

    assert result.id == message_id


async def test_list_messages(async_mpt_ops):
    service = async_mpt_ops.notifications.messages

    result = await service.fetch_page(limit=1)

    assert len(result) > 0


async def test_not_found(async_mpt_client, invalid_message_id):
    service = async_mpt_client.notifications.messages

    with pytest.raises(MPTAPIError):
        await service.get(invalid_message_id)

import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


async def test_get_message(async_mpt_client, message_id):
    service = async_mpt_client.notifications.messages

    result = await service.get(message_id)

    assert result.id == message_id


async def test_list_messages(async_mpt_client):
    service = async_mpt_client.notifications.messages

    result = service.fetch_page(limit=2)

    assert len(result) > 2


async def test_not_found(async_mpt_vendor):
    service = async_mpt_vendor.notifications.messages

    with pytest.raises(MPTAPIError):
        await service.get("MSG-000-000-000")

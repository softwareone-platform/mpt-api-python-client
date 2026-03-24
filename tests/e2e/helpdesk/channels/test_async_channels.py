import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_get_channel(async_mpt_ops, channel_id):
    service = async_mpt_ops.helpdesk.channels

    result = await service.get(channel_id)

    assert result.id == channel_id


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_list_channels(async_mpt_ops):
    service = async_mpt_ops.helpdesk.channels

    result = await service.fetch_page(limit=1)

    assert len(result) > 0


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_create_channel(async_created_channel):
    result = async_created_channel

    assert result.id is not None


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_update_channel(async_mpt_ops, async_created_channel, short_uuid):
    service = async_mpt_ops.helpdesk.channels
    new_name = f"E2E Updated Channel {short_uuid}"

    result = await service.update(async_created_channel.id, {"name": new_name})

    assert result.id == async_created_channel.id
    assert result.to_dict().get("name") == new_name


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_delete_channel(async_mpt_ops, async_created_channel):
    result = async_created_channel

    await async_mpt_ops.helpdesk.channels.delete(result.id)


async def test_not_found(async_mpt_ops, invalid_channel_id):
    service = async_mpt_ops.helpdesk.channels

    with pytest.raises(MPTAPIError):
        await service.get(invalid_channel_id)

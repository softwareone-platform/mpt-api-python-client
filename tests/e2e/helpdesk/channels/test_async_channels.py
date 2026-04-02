from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.helpdesk.channels import Channel

pytestmark = [pytest.mark.flaky, pytest.mark.skip(reason="Unskip after MPT-19124 completed")]


async def test_get_channel(async_mpt_ops, channel_id):
    service = async_mpt_ops.helpdesk.channels

    result = await service.get(channel_id)

    assert isinstance(result, Channel)


async def test_list_channels(async_mpt_ops):
    service = async_mpt_ops.helpdesk.channels

    result = await service.fetch_page(limit=1)

    assert len(result) > 0
    assert all(isinstance(channel, Channel) for channel in result)


def test_create_channel(async_created_channel):
    result = async_created_channel

    assert isinstance(result, Channel)


async def test_update_channel(async_mpt_ops, async_created_channel, short_uuid):
    service = async_mpt_ops.helpdesk.channels
    new_name = f"E2E Updated Channel {short_uuid}"

    result = await service.update(async_created_channel.id, {"name": new_name})

    assert isinstance(result, Channel)
    assert result.to_dict().get("name") == new_name


async def test_delete_channel(async_mpt_ops, async_created_channel):
    result = async_created_channel

    await async_mpt_ops.helpdesk.channels.delete(result.id)


async def test_not_found(async_mpt_ops, invalid_channel_id):
    service = async_mpt_ops.helpdesk.channels

    with pytest.raises(MPTAPIError) as error:
        await service.get(invalid_channel_id)
    assert error.value.status_code == HTTPStatus.NOT_FOUND

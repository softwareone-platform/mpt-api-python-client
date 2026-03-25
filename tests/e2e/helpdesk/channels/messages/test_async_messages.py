import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_list_channel_messages(async_channel_messages_service):
    result = await async_channel_messages_service.fetch_page(limit=1)

    assert len(result) > 0


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_list_channel_messages_not_found(async_mpt_ops, invalid_channel_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.helpdesk.channels.messages(invalid_channel_id).fetch_page(limit=1)

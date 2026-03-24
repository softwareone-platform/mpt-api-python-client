import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_get_channel(mpt_ops, channel_id):
    service = mpt_ops.helpdesk.channels

    result = service.get(channel_id)

    assert result.id == channel_id


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_list_channels(mpt_ops):
    service = mpt_ops.helpdesk.channels

    result = service.fetch_page(limit=1)

    assert len(result) > 0


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_create_channel(created_channel):
    result = created_channel

    assert result.id is not None


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_update_channel(mpt_ops, created_channel, short_uuid):
    service = mpt_ops.helpdesk.channels
    new_name = f"E2E Updated Channel {short_uuid}"

    result = service.update(created_channel.id, {"name": new_name})

    assert result.id == created_channel.id
    assert result.to_dict().get("name") == new_name


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_delete_channel(mpt_ops, created_channel):
    result = created_channel

    mpt_ops.helpdesk.channels.delete(result.id)


def test_not_found(mpt_ops, invalid_channel_id):
    service = mpt_ops.helpdesk.channels

    with pytest.raises(MPTAPIError):
        service.get(invalid_channel_id)

from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.helpdesk.channels import Channel

pytestmark = [pytest.mark.flaky, pytest.mark.skip(reason="Unskip when MPT-19696 unblocked")]


def test_get_channel(mpt_ops, channel_id):
    service = mpt_ops.helpdesk.channels

    result = service.get(channel_id)

    assert isinstance(result, Channel)


def test_list_channels(mpt_ops):
    service = mpt_ops.helpdesk.channels

    result = service.fetch_page(limit=1)

    assert len(result) > 0
    assert all(isinstance(channel, Channel) for channel in result)


def test_create_channel(created_channel):
    result = created_channel

    assert isinstance(result, Channel)


def test_update_channel(mpt_ops, created_channel, short_uuid):
    service = mpt_ops.helpdesk.channels
    new_name = f"E2E Updated Channel {short_uuid}"

    result = service.update(created_channel.id, {"name": new_name})

    assert isinstance(result, Channel)
    assert result.to_dict().get("name") == new_name


def test_delete_channel(mpt_ops, created_channel):
    result = created_channel

    mpt_ops.helpdesk.channels.delete(result.id)


def test_not_found(mpt_ops, invalid_channel_id):
    service = mpt_ops.helpdesk.channels

    with pytest.raises(MPTAPIError) as error:
        service.get(invalid_channel_id)

    assert error.value.status_code == HTTPStatus.NOT_FOUND

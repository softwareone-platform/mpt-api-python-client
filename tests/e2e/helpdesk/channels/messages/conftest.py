import pytest


@pytest.fixture
def channel_messages_service(mpt_ops, channel_id):
    return mpt_ops.helpdesk.channels.messages(channel_id)


@pytest.fixture
def async_channel_messages_service(async_mpt_ops, channel_id):
    return async_mpt_ops.helpdesk.channels.messages(channel_id)

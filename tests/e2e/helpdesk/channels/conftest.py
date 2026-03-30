import pytest

from tests.e2e.helper import (
    async_create_fixture_resource_and_delete,
    create_fixture_resource_and_delete,
)


@pytest.fixture(scope="session")
def channel_id(e2e_config):
    return e2e_config["helpdesk.channel.id"]  # FIXME: seed data


@pytest.fixture(scope="session")
def invalid_channel_id():
    return "CHN-0000-0000-0000"


@pytest.fixture
def channel_data(short_uuid):
    return {"name": f"E2E Channel {short_uuid}"}


@pytest.fixture
def created_channel(mpt_ops, channel_data):
    with create_fixture_resource_and_delete(mpt_ops.helpdesk.channels, channel_data) as channel:
        yield channel


@pytest.fixture
async def async_created_channel(async_mpt_ops, channel_data):
    async with async_create_fixture_resource_and_delete(
        async_mpt_ops.helpdesk.channels, channel_data
    ) as channel:
        yield channel

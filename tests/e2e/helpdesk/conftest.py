import pytest

from tests.e2e.helper import (
    async_create_fixture_resource_and_delete,
    create_fixture_resource_and_delete,
)


@pytest.fixture
def queue_data(short_uuid):
    return {
        "name": f"E2E Queue {short_uuid}",
        "description": "E2E Created Helpdesk Queue",
        "internal": False,
    }


@pytest.fixture(scope="session")
def invalid_queue_id():
    return "HQU-0000-0000"


@pytest.fixture
def created_queue(mpt_ops, queue_data):
    with create_fixture_resource_and_delete(mpt_ops.helpdesk.queues, queue_data) as queue:
        yield queue


@pytest.fixture
def created_disabled_queue(mpt_ops, created_queue):
    result = mpt_ops.helpdesk.queues.disable(created_queue.id)
    assert result.status == "Disabled"

    return result


@pytest.fixture
async def async_created_queue(async_mpt_ops, queue_data):
    async with async_create_fixture_resource_and_delete(
        async_mpt_ops.helpdesk.queues, queue_data
    ) as queue:
        yield queue


@pytest.fixture
async def async_created_disabled_queue(async_mpt_ops, async_created_queue):
    result = await async_mpt_ops.helpdesk.queues.disable(async_created_queue.id)
    assert result.status == "Disabled"

    return result

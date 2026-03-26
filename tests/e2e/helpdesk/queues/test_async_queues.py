from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.helpdesk.queues import Queue

pytestmark = [pytest.mark.flaky]


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_get_queue(async_mpt_ops, async_created_queue):
    result = await async_mpt_ops.helpdesk.queues.get(async_created_queue.id)

    assert result.id == async_created_queue.id


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_list_queues(async_mpt_ops):
    result = await async_mpt_ops.helpdesk.queues.fetch_page(limit=1)

    assert len(result) > 0
    assert all(isinstance(queue, Queue) for queue in result)


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_create_queue(async_created_queue):
    result = async_created_queue

    assert result is not None


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_update_queue(async_mpt_ops, async_created_queue, short_uuid):
    update_data = {"description": f"e2e update {short_uuid}"}

    result = await async_mpt_ops.helpdesk.queues.update(async_created_queue.id, update_data)

    assert result.id == async_created_queue.id
    assert result.to_dict().get("description") == update_data["description"]


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_activate_queue(async_mpt_ops, async_created_queue):
    result = await async_mpt_ops.helpdesk.queues.activate(async_created_queue.id)

    assert result is not None


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_disable_queue(async_mpt_ops, async_created_queue):
    result = await async_mpt_ops.helpdesk.queues.disable(async_created_queue.id)

    assert result is not None


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_delete_queue(async_mpt_ops, async_created_queue):
    await async_mpt_ops.helpdesk.queues.delete(async_created_queue.id)  # act


async def test_not_found(async_mpt_ops, invalid_queue_id):
    with pytest.raises(MPTAPIError) as error:
        await async_mpt_ops.helpdesk.queues.get(invalid_queue_id)
    assert error.value.status_code == HTTPStatus.NOT_FOUND

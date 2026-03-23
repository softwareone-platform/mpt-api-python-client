import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_get_queue(mpt_ops, created_queue):
    result = mpt_ops.helpdesk.queues.get(created_queue.id)

    assert result.id == created_queue.id


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_list_queues(mpt_ops):
    result = mpt_ops.helpdesk.queues.fetch_page(limit=1)

    assert len(result) > 0


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_create_queue(created_queue):
    result = created_queue

    assert result is not None


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_update_queue(mpt_ops, created_queue, short_uuid):
    update_data = {"description": f"e2e update {short_uuid}"}

    result = mpt_ops.helpdesk.queues.update(created_queue.id, update_data)

    assert result.id == created_queue.id
    assert result.to_dict().get("description") == update_data["description"]


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_activate_queue(mpt_ops, created_queue):
    result = mpt_ops.helpdesk.queues.activate(created_queue.id)

    assert result is not None


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_disable_queue(mpt_ops, created_queue):
    result = mpt_ops.helpdesk.queues.disable(created_queue.id)

    assert result is not None


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_delete_queue(mpt_ops, created_queue):
    mpt_ops.helpdesk.queues.delete(created_queue.id)  # act


def test_not_found(mpt_ops, invalid_queue_id):
    with pytest.raises(MPTAPIError):
        mpt_ops.helpdesk.queues.get(invalid_queue_id)

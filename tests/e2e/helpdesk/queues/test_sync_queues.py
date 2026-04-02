from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.helpdesk.queues import Queue

pytestmark = [pytest.mark.flaky]


def test_get_queue(mpt_ops, created_queue):
    result = mpt_ops.helpdesk.queues.get(created_queue.id)

    assert isinstance(result, Queue)


def test_list_queues(mpt_ops):
    result = mpt_ops.helpdesk.queues.fetch_page(limit=1)

    assert len(result) > 0
    assert all(isinstance(queue, Queue) for queue in result)


def test_create_queue(created_queue):
    result = created_queue

    assert isinstance(result, Queue)


def test_update_queue(mpt_ops, created_queue, short_uuid):
    update_data = {"description": f"e2e update {short_uuid}"}

    result = mpt_ops.helpdesk.queues.update(created_queue.id, update_data)

    assert isinstance(result, Queue)
    assert result.to_dict().get("description") == update_data["description"]


def test_activate_queue(mpt_ops, created_disabled_queue):
    result = mpt_ops.helpdesk.queues.activate(created_disabled_queue.id)

    assert result.status == "Active"


def test_disable_queue(mpt_ops, created_queue):
    result = mpt_ops.helpdesk.queues.disable(created_queue.id)

    assert result.status == "Disabled"


def test_delete_queue(mpt_ops, created_queue):
    mpt_ops.helpdesk.queues.delete(created_queue.id)  # act


def test_not_found(mpt_ops, invalid_queue_id):
    with pytest.raises(MPTAPIError) as error:
        mpt_ops.helpdesk.queues.get(invalid_queue_id)

    assert error.value.status_code == HTTPStatus.NOT_FOUND

import pytest


def _queue_id_from_case(case):
    case_data = case.to_dict()
    queue_data = case_data.get("queue")
    if not isinstance(queue_data, dict):
        return None

    queue_id = queue_data.get("id")
    if not isinstance(queue_id, str):
        return None

    return queue_id


@pytest.fixture
def queue_id(mpt_ops):
    cases = mpt_ops.helpdesk.cases.fetch_page(limit=1)
    if not cases:
        pytest.skip("No support case available to infer queue for create test.")

    queue_id = _queue_id_from_case(cases[0])
    if queue_id is None:
        pytest.skip("No queue id available to create support case.")

    return queue_id


@pytest.fixture
def case_data(queue_id):
    return {"queue": {"id": queue_id}}


@pytest.fixture
def case_update_data():
    return {"awaiting": True}

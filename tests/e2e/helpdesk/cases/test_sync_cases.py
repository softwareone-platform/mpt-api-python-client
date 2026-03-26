from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.helpdesk.cases import Case

pytestmark = [pytest.mark.flaky]


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_get_case(mpt_ops, created_case):
    result = mpt_ops.helpdesk.cases.get(created_case.id)

    assert result.id == created_case.id


def test_list_cases(mpt_ops):
    limit = 1

    result = mpt_ops.helpdesk.cases.fetch_page(limit=limit)

    assert len(result) > 0
    assert all(isinstance(case, Case) for case in result)


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_create_case(created_case):
    result = created_case

    assert result is not None


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_update_case(mpt_ops, created_case, short_uuid):
    update_data = {"description": f"e2e update {short_uuid}"}

    result = mpt_ops.helpdesk.cases.update(created_case.id, update_data)

    assert result.id == created_case.id
    assert result.to_dict().get("description") == update_data["description"]


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_process_case(mpt_ops, created_case):
    result = mpt_ops.helpdesk.cases.process(created_case.id)

    assert result is not None


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_query_case(mpt_ops, created_case):
    processed_case = mpt_ops.helpdesk.cases.process(created_case.id)

    result = mpt_ops.helpdesk.cases.query(
        processed_case.id, {"queryPrompt": "Could you provide more details?"}
    )

    assert result is not None


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_complete_case(mpt_ops, created_case):
    processed_case = mpt_ops.helpdesk.cases.process(created_case.id)

    result = mpt_ops.helpdesk.cases.complete(processed_case.id)

    assert result is not None


def test_not_found(mpt_ops, invalid_case_id):
    with pytest.raises(MPTAPIError) as error:
        mpt_ops.helpdesk.cases.get(invalid_case_id)

    assert error.value.status_code == HTTPStatus.NOT_FOUND

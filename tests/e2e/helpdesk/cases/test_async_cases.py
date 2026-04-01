from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.helpdesk.cases import Case

pytestmark = [pytest.mark.flaky]


async def test_get_case(async_mpt_ops, async_created_case):
    result = await async_mpt_ops.helpdesk.cases.get(async_created_case.id)

    assert result.id == async_created_case.id


async def test_list_cases(async_mpt_ops):
    limit = 1

    result = await async_mpt_ops.helpdesk.cases.fetch_page(limit=limit)

    assert len(result) > 0
    assert all(isinstance(case, Case) for case in result)


def test_create_case(async_created_case):
    result = async_created_case

    assert result is not None


async def test_update_case(async_mpt_ops, async_created_case, short_uuid):
    assert async_created_case.to_dict().get("awaiting") is False
    update_data = {"awaiting": True}

    result = await async_mpt_ops.helpdesk.cases.update(async_created_case.id, update_data)

    assert result.id == async_created_case.id
    assert result.to_dict().get("awaiting") is True


def test_process_case(async_mpt_ops, async_processed_case):
    result = async_processed_case.to_dict().get("status")

    assert result == "Processing"


def test_query_case(async_mpt_ops, async_queried_case):
    result = async_queried_case.to_dict().get("status")

    assert result == "Querying"


async def test_complete_case(async_mpt_ops, async_processed_case):
    result = await async_mpt_ops.helpdesk.cases.complete(async_processed_case.id)

    assert result.to_dict().get("status") == "Completed"


async def test_not_found(async_mpt_ops, invalid_case_id):
    with pytest.raises(MPTAPIError) as error:
        await async_mpt_ops.helpdesk.cases.get(invalid_case_id)
    assert error.value.status_code == HTTPStatus.NOT_FOUND

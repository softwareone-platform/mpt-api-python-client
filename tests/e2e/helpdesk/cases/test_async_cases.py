import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_get_case(async_mpt_ops, async_created_case):
    result = await async_mpt_ops.helpdesk.cases.get(async_created_case.id)

    assert result.id == async_created_case.id


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_list_cases(async_mpt_ops):
    limit = 1

    result = await async_mpt_ops.helpdesk.cases.fetch_page(limit=limit)

    assert len(result) > 0


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
def test_create_case(async_created_case):
    result = async_created_case

    assert result is not None


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_update_case(async_mpt_ops, async_created_case, short_uuid):
    update_data = {"description": f"e2e update {short_uuid}"}

    result = await async_mpt_ops.helpdesk.cases.update(async_created_case.id, update_data)

    assert result.id == async_created_case.id
    assert result.to_dict().get("description") == update_data["description"]


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_process_case(async_mpt_ops, async_created_case):
    result = await async_mpt_ops.helpdesk.cases.process(async_created_case.id)

    assert result is not None


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_query_case(async_mpt_ops, async_created_case):
    processed_case = await async_mpt_ops.helpdesk.cases.process(async_created_case.id)

    result = await async_mpt_ops.helpdesk.cases.query(
        processed_case.id, {"queryPrompt": "Could you provide more details?"}
    )

    assert result is not None


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_complete_case(async_mpt_ops, async_created_case):
    processed_case = await async_mpt_ops.helpdesk.cases.process(async_created_case.id)

    result = await async_mpt_ops.helpdesk.cases.complete(processed_case.id)

    assert result is not None


@pytest.mark.skip(reason="Unskip after MPT-19124 completed")
async def test_not_found(async_mpt_ops, invalid_case_id):
    with pytest.raises(MPTAPIError):
        await async_mpt_ops.helpdesk.cases.get(invalid_case_id)

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def credit_memos(async_mpt_ops):
    limit = 1
    return await async_mpt_ops.billing.credit_memos.fetch_page(limit=limit)


@pytest.fixture
def credit_memo(credit_memos):
    if credit_memos:
        return credit_memos[0]
    return None


async def test_get_credit_memo_by_id(async_mpt_ops, credit_memo):
    if credit_memo is None:
        pytest.skip("No credit memos available to test retrieval by ID.")
    credit_memo_id = credit_memo.id

    result = await async_mpt_ops.billing.credit_memos.get(credit_memo_id)

    assert result is not None


async def test_get_credit_memo_by_id_not_found(async_mpt_ops, invalid_credit_memo_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.billing.credit_memos.get(invalid_credit_memo_id)


async def test_list_credit_memos(async_mpt_ops):
    limit = 10

    result = await async_mpt_ops.billing.credit_memos.fetch_page(limit=limit)

    assert len(result) > 0


async def test_filter_credit_memos(async_mpt_ops, credit_memo):
    if credit_memo is None:
        pytest.skip("No credit memos available to test filtering.")
    credit_memo_id = credit_memo.id
    credit_memo_status = credit_memo.status
    select_fields = ["-vendor"]
    filtered_credit_memos = (
        async_mpt_ops.billing.credit_memos.filter(RQLQuery(id=credit_memo_id))
        .filter(RQLQuery(status=credit_memo_status))
        .select(*select_fields)
    )

    result = [credit_memo async for credit_memo in filtered_credit_memos.iterate()]

    assert len(result) == 1

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def created_credit_memo(async_mpt_client, credit_memo_factory):
    new_credit_memo_request_data = credit_memo_factory()

    return await async_mpt_client.commerce.credit_memos.create(new_credit_memo_request_data)


async def test_get_credit_memo_by_id(async_mpt_client, credit_memo_id):
    result = await async_mpt_client.commerce.credit_memos.get(credit_memo_id)
    assert result is not None


async def test_get_credit_memo_by_id_not_found(async_mpt_client, invalid_credit_memo_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_client.commerce.credit_memos.get(invalid_credit_memo_id)


async def test_list_credit_memos(async_mpt_client):
    limit = 10

    result = await async_mpt_client.commerce.credit_memos.fetch_page(limit=limit)

    assert len(result) > 0


async def test_filter_credit_memos(async_mpt_client, credit_memo_id):
    select_fields = ["-vendor"]
    filtered_credit_memos = (
        await async_mpt_client.commerce.credit_memos.filter(RQLQuery(id=credit_memo_id))
        .filter(RQLQuery(status="Issued"))
        .select(*select_fields)
    )

    result = list(filtered_credit_memos.iterate())

    assert len(result) == 1


def test_create_credit_memo(created_credit_memo):
    result = created_credit_memo

    assert result is not None

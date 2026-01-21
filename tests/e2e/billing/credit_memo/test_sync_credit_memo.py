import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def credit_memos(mpt_ops):
    limit = 1
    return mpt_ops.billing.credit_memos.fetch_page(limit=limit)


@pytest.fixture
def credit_memo(credit_memos):
    if credit_memos:
        return credit_memos[0]
    return None


def test_get_credit_memo_by_id(mpt_ops, credit_memo):
    if credit_memo is None:
        pytest.skip("No credit memos available to test retrieval by ID.")
    credit_memo_id = credit_memo.id

    result = mpt_ops.billing.credit_memos.get(credit_memo_id)

    assert result is not None


def test_get_credit_memo_by_id_not_found(mpt_ops, invalid_credit_memo_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_ops.billing.credit_memos.get(invalid_credit_memo_id)


def test_list_credit_memos(mpt_ops):
    limit = 10

    result = mpt_ops.billing.credit_memos.fetch_page(limit=limit)

    assert len(result) > 0


def test_filter_credit_memos(mpt_ops, credit_memo):
    if credit_memo is None:
        pytest.skip("No credit memos available to test filtering.")
    credit_memo_id = credit_memo.id
    credit_memo_status = credit_memo.status
    select_fields = ["-vendor"]
    filtered_credit_memos = (
        mpt_ops.billing.credit_memos
        .filter(RQLQuery(id=credit_memo_id))
        .filter(RQLQuery(status=credit_memo_status))
        .select(*select_fields)
    )

    result = list(filtered_credit_memos.iterate())

    assert len(result) == 1

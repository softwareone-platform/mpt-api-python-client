import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


def test_get_billing_ledger_by_id(mpt_ops, ledger_id):
    result = mpt_ops.billing.ledgers.get(ledger_id)

    assert result is not None


def test_list_billing_ledgers(mpt_ops):
    limit = 10

    result = mpt_ops.billing.ledgers.fetch_page(limit=limit)

    assert len(result) > 0


def test_get_billing_ledger_by_id_not_found(mpt_ops, invalid_ledger_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_ops.billing.ledgers.get(invalid_ledger_id)


def test_filter_billing_ledgers(mpt_ops, ledger_id, commerce_product_id):
    select_fields = ["-authorization"]
    filtered_ledgers = (
        mpt_ops.billing.ledgers.filter(RQLQuery(id=ledger_id))
        .filter(RQLQuery(f"product.id={commerce_product_id}"))
        .select(*select_fields)
    )

    result = list(filtered_ledgers.iterate())

    assert len(result) > 0

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


async def test_get_billing_ledger_by_id(async_mpt_ops, ledger_id):
    result = await async_mpt_ops.billing.ledgers.get(ledger_id)

    assert result is not None


async def test_list_billing_ledgers(async_mpt_ops):
    limit = 10

    result = await async_mpt_ops.billing.ledgers.fetch_page(limit=limit)

    assert len(result) > 0


async def test_get_billing_ledger_by_id_not_found(async_mpt_ops, invalid_ledger_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.billing.ledgers.get(invalid_ledger_id)


async def test_filter_billing_ledgers(async_mpt_ops, ledger_id, commerce_product_id):
    select_fields = ["-authorization"]
    filtered_ledgers = (
        async_mpt_ops.billing.ledgers
        .filter(RQLQuery(id=ledger_id))
        .filter(RQLQuery(f"product.id={commerce_product_id}"))
        .select(*select_fields)
    )

    result = [ledger async for ledger in filtered_ledgers.iterate()]

    assert len(result) > 0

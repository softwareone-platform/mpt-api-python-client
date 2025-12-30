import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def created_billing_ledger(async_mpt_vendor, billing_ledger_factory):
    new_billing_ledger_request_data = billing_ledger_factory()

    return await async_mpt_vendor.billing.ledgers.create(new_billing_ledger_request_data)


async def test_get_billing_ledger_by_id(async_mpt_vendor, billing_ledger_id):
    result = await async_mpt_vendor.billing.ledgers.get(billing_ledger_id)

    assert result is not None


async def test_list_billing_ledgers(async_mpt_vendor):
    limit = 10

    result = await async_mpt_vendor.billing.ledgers.fetch_page(limit=limit)

    assert len(result) > 0


async def test_get_billing_ledger_by_id_not_found(async_mpt_vendor, invalid_ledger_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_vendor.billing.ledgers.get(invalid_ledger_id)


async def test_filter_billing_ledgers(async_mpt_vendor, billing_ledger_id, commerce_product_id):
    select_fields = ["-authorization"]
    filtered_ledgers = (
        await async_mpt_vendor.billing.ledgers.filter(RQLQuery(id=billing_ledger_id))
        .filter(RQLQuery(f"product.id={commerce_product_id}"))
        .select(*select_fields)
    )

    result = [ledger async for ledger in filtered_ledgers.iterate()]

    assert len(result) > 0


def test_create_billing_ledger(created_billing_ledger):
    result = created_billing_ledger

    assert result is not None


async def test_update_billing_ledger(async_mpt_vendor, created_billing_ledger, billing_ledger_factory):
    updated_data = billing_ledger_factory()

    result = await async_mpt_vendor.billing.ledgers.update(created_billing_ledger.id, updated_data)

    assert result is not None


async def test_recalculate_billing_ledger(async_mpt_vendor, created_billing_ledger):
    result = await async_mpt_vendor.billing.ledgers.recalculate(created_billing_ledger.id)

    assert result is not None


async def test_accept_billing_ledger(async_mpt_vendor, created_billing_ledger):
    result = await async_mpt_vendor.billing.ledgers.accept(created_billing_ledger.id)

    assert result is not None


async def test_queue_billing_ledger(async_mpt_vendor, created_billing_ledger):
    result = await async_mpt_vendor.billing.ledgers.queue(created_billing_ledger.id)

    assert result is not None

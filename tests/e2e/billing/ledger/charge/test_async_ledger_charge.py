import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def ledger_charges(async_mpt_ops, ledger_id):
    return async_mpt_ops.billing.ledgers.charges(ledger_id)


async def test_get_ledger_charge_by_id(ledger_charges, ledger_charge_id):
    result = await ledger_charges.get(ledger_charge_id)

    assert result is not None


async def test_get_ledger_charge_by_id_not_found(ledger_charges, invalid_ledger_charge_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await ledger_charges.get(invalid_ledger_charge_id)


async def test_list_ledger_charges(ledger_charges):
    limit = 10

    result = await ledger_charges.fetch_page(limit=limit)

    assert len(result) > 0


async def test_filter_ledger_charges(ledger_charges, ledger_charge_id):
    select_fields = ["-journal"]
    filtered_charges = (
        ledger_charges.filter(RQLQuery(id=ledger_charge_id))
        .filter(RQLQuery(externalIds__invoice="INV12345"))
        .select(*select_fields)
    )

    result = [charges async for charges in filtered_charges.iterate()]

    assert len(result) > 0

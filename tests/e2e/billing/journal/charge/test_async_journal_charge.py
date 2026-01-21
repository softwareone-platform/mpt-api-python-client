import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def journal_charges(async_mpt_vendor, billing_journal_id):
    return async_mpt_vendor.billing.journals.charges(billing_journal_id)


async def test_get_journal_charge_by_id(journal_charges, journal_charge_id):
    result = await journal_charges.get(journal_charge_id)

    assert result is not None


async def test_get_journal_charge_by_id_not_found(journal_charges, invalid_journal_charge_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await journal_charges.get(invalid_journal_charge_id)


async def test_list_journal_charges(journal_charges):
    limit = 10

    result = await journal_charges.fetch_page(limit=limit)

    assert len(result) > 0


async def test_filter_journal_charges(journal_charges, journal_charge_id):
    select_fields = ["-period"]
    filtered_charges = (
        journal_charges
        .filter(RQLQuery(id=journal_charge_id))
        .filter(RQLQuery(externalIds__invoice="INV12345"))
        .select(*select_fields)
    )

    result = [charges async for charges in filtered_charges.iterate()]

    assert len(result) == 1

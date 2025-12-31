import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


async def test_get_journal_charge_by_id(journal_charges, journal_charge_id):
    result = journal_charges.get(journal_charge_id)

    assert result is not None


async def test_get_journal_charge_by_id_not_found(journal_charges, invalid_journal_charge_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        journal_charges.get(invalid_journal_charge_id)


async def test_list_journal_charges(journal_charges):
    limit = 10

    result = journal_charges.fetch_page(limit=limit)

    assert len(result) > 0


async def test_filter_journal_charges(journal_charges, journal_charge_id):
    select_fields = ["-period"]
    filtered_charges = (
        journal_charges.filter(RQLQuery(id=journal_charge_id))
        .filter(RQLQuery(saleDetails__orderQty__eq="COM"))
        .select(*select_fields)
    )

    result = list(filtered_charges.iterate())

    assert len(result) == 1

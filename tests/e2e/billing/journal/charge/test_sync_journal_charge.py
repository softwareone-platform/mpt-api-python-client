import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def journal_charges(mpt_vendor, billing_journal_id):
    return mpt_vendor.billing.journals.charges(billing_journal_id)


def test_get_journal_charge_by_id(journal_charges, journal_charge_id):
    result = journal_charges.get(journal_charge_id)

    assert result is not None


def test_get_journal_charge_by_id_not_found(journal_charges, invalid_journal_charge_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        journal_charges.get(invalid_journal_charge_id)


def test_list_journal_charges(journal_charges):
    limit = 10

    result = journal_charges.fetch_page(limit=limit)

    assert len(result) > 0


def test_filter_journal_charges(journal_charges, journal_charge_id):
    select_fields = ["-period"]
    filtered_charges = (
        journal_charges
        .filter(RQLQuery(id=journal_charge_id))
        .filter(RQLQuery(externalIds__invoice="INV12345"))
        .select(*select_fields)
    )

    result = list(filtered_charges.iterate())

    assert len(result) == 1

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def ledger_charges(mpt_ops, ledger_id):
    return mpt_ops.billing.ledgers.charges(ledger_id)


def test_get_ledger_charge_by_id(ledger_charges, ledger_charge_id):
    result = ledger_charges.get(ledger_charge_id)

    assert result is not None


def test_get_ledger_charge_by_id_not_found(ledger_charges, invalid_ledger_charge_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        ledger_charges.get(invalid_ledger_charge_id)


def test_list_ledger_charges(ledger_charges):
    limit = 10

    result = ledger_charges.fetch_page(limit=limit)

    assert len(result) > 0


def test_filter_ledger_charges(ledger_charges, ledger_charge_id):
    select_fields = ["-journal"]
    filtered_charges = (
        ledger_charges.filter(RQLQuery(id=ledger_charge_id))
        .filter(RQLQuery(externalIds__invoice="INV12345"))
        .select(*select_fields)
    )

    result = list(filtered_charges.iterate())

    assert len(result) > 0

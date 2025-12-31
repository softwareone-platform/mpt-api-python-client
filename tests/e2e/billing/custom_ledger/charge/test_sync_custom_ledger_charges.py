import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def custom_ledger_charges(mpt_ops, custom_ledger_id):
    return mpt_ops.billing.custom_ledgers.charges(custom_ledger_id)


def test_get_custom_ledger_charge_by_id(custom_ledger_charges, custom_ledger_charge_id):
    result = custom_ledger_charges.get(custom_ledger_charge_id)

    assert result is not None


def test_get_custom_ledger_charge_by_id_not_found(
    custom_ledger_charges, invalid_custom_ledger_charge_id
):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        custom_ledger_charges.get(invalid_custom_ledger_charge_id)


def test_list_custom_ledger_charges(custom_ledger_charges):
    limit = 10

    result = custom_ledger_charges.fetch_page(limit=limit)

    assert len(result) > 0


def test_filter_custom_ledger_charges(custom_ledger_charges, custom_ledger_charge_id):
    select_fields = ["-price"]
    filtered_charges = (
        custom_ledger_charges.filter(RQLQuery(id=custom_ledger_charge_id))
        .filter(RQLQuery(description__value2="Description 2"))
        .select(*select_fields)
    )

    result = list(filtered_charges.iterate())

    assert len(result) == 1

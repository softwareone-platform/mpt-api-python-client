import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def statement_charges(async_mpt_ops, statement_id):
    return async_mpt_ops.billing.statements.charges(statement_id)


async def test_get_statement_charge_by_id(statement_charges, statement_charge_id):
    result = await statement_charges.get(statement_charge_id)

    assert result is not None


async def test_get_statement_charge_by_id_not_found(statement_charges, invalid_statement_charge_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await statement_charges.get(invalid_statement_charge_id)


async def test_list_statement_charges(statement_charges):
    limit = 10

    result = await statement_charges.fetch_page(limit=limit)

    assert len(result) > 0


async def test_filter_statement_charges(statement_charges, statement_charge_id):
    select_fields = ["-price"]
    filtered_charges = (
        statement_charges.filter(RQLQuery(id=statement_charge_id))
        .filter(RQLQuery(externalIds__invoice="INV12345"))
        .select(*select_fields)
    )

    result = [statement async for statement in filtered_charges.iterate()]

    assert len(result) == 1

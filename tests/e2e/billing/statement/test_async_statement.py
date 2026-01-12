import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


async def test_get_statement_by_id(async_mpt_ops, statement_id):
    result = await async_mpt_ops.billing.statements.get(statement_id)

    assert result is not None


async def test_list_statements(async_mpt_ops):
    limit = 10

    result = await async_mpt_ops.billing.statements.fetch_page(limit=limit)

    assert len(result) > 0


async def test_get_statement_by_id_not_found(async_mpt_ops, invalid_statement_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.billing.statements.get(invalid_statement_id)


async def test_filter_statements(async_mpt_ops, statement_id):
    select_fields = ["-client"]
    filtered_statements = (
        async_mpt_ops.billing.statements.filter(RQLQuery(id=statement_id))
        .filter(RQLQuery(type="Debit"))
        .select(*select_fields)
    )

    result = [statement async for statement in filtered_statements.iterate()]

    assert len(result) == 1

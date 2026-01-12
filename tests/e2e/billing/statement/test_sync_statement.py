import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


def test_get_statement_by_id(mpt_ops, statement_id):
    result = mpt_ops.billing.statements.get(statement_id)

    assert result is not None


def test_list_statements(mpt_ops):
    limit = 10

    result = mpt_ops.billing.statements.fetch_page(limit=limit)

    assert len(result) > 0


def test_get_statement_by_id_not_found(mpt_ops, invalid_statement_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_ops.billing.statements.get(invalid_statement_id)


def test_filter_statements(mpt_ops, statement_id):
    select_fields = ["-client"]
    filtered_statements = (
        mpt_ops.billing.statements.filter(RQLQuery(id=statement_id))
        .filter(RQLQuery(type="Debit"))
        .select(*select_fields)
    )

    result = list(filtered_statements.iterate())

    assert len(result) == 1

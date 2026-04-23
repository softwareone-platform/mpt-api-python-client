import pytest

from mpt_api_client import RQLQuery
from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


def test_get_query_by_id(mpt_ops, spotlight_query_id):
    result = mpt_ops.spotlight.queries.get(spotlight_query_id)

    assert result.id == spotlight_query_id


def test_get_query_invalid_id(mpt_ops, invalid_spotlight_query_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_ops.spotlight.queries.get(invalid_spotlight_query_id)


def test_list_queries(mpt_ops):
    limit = 10

    result = mpt_ops.spotlight.queries.fetch_page(limit=limit)

    assert len(result) > 0


def test_filter_and_select_queries(mpt_ops, spotlight_query_id):
    select_fields = ["-template", "-invalidationInterval", "-invalidateOnDateChange"]
    filtered_spotlight_queries = mpt_ops.spotlight.queries.filter(
        RQLQuery(id=spotlight_query_id)
    ).select(*select_fields)

    result = list(filtered_spotlight_queries.iterate())

    assert len(result) == 1

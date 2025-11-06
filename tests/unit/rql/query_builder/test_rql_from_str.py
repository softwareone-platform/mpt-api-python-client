from mpt_api_client import RQLQuery


def test_rql_from_str():
    str_query = "eq(id,ID)"

    rql = RQLQuery.from_string(str_query)

    assert str(rql) == str_query

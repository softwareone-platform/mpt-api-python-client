import pytest

from mpt_api_client.http.query_state import QueryState


@pytest.fixture
def query_state():
    return QueryState()


def test_filter_init(filter_status_active):
    result = QueryState(
        rql=filter_status_active, select=["agreement", "-product"], order_by=["-created", "name"]
    )

    assert result.filter == filter_status_active
    assert result.select == ["agreement", "-product"]
    assert result.order_by == ["-created", "name"]


def test_build_url(filter_status_active):
    query_state = QueryState(
        rql=filter_status_active,
        select=["-audit", "product.agreements", "-product.agreements.product"],
        order_by=["-created", "name"],
    )

    result = query_state.build()

    assert result == (
        "order=-created,name"
        "&select=-audit,product.agreements,-product.agreements.product"
        "&eq(status,active)"
    )


def test_empty_build(query_state):
    result = query_state.build()

    assert not result


def test_build_with_params(filter_status_active):
    query_state = QueryState(rql=filter_status_active, order_by=["created"], select=["name"])
    query_params = {"limit": "10"}

    result = query_state.build(query_params)

    assert result == "limit=10&order=created&select=name&eq(status,active)"

import pytest

from mpt_api_client.rql.query_builder import RQLQuery


def test_filter(collection_client):
    filter_query = RQLQuery(status="active")

    new_collection = collection_client.filter(filter_query)

    assert collection_client.query_rql is None
    assert new_collection != collection_client
    assert new_collection.query_rql == filter_query


def test_multiple_filters(collection_client) -> None:
    filter_query = RQLQuery(status="active")
    filter_query2 = RQLQuery(name="test")

    new_collection = collection_client.filter(filter_query).filter(filter_query2)

    assert collection_client.query_rql is None
    assert new_collection.query_rql == filter_query & filter_query2


def test_select(collection_client) -> None:
    new_collection = collection_client.select("agreement", "-product")

    assert collection_client.query_select is None
    assert new_collection != collection_client
    assert new_collection.query_select == ["agreement", "-product"]


def test_select_exception(collection_client) -> None:
    with pytest.raises(ValueError):
        collection_client.select("agreement").select("product")


def test_order_by(collection_client):
    new_collection = collection_client.order_by("created", "-name")

    assert collection_client.query_order_by is None
    assert new_collection != collection_client
    assert new_collection.query_order_by == ["created", "-name"]


def test_order_by_exception(collection_client):
    with pytest.raises(
        ValueError, match=r"Ordering is already set. Cannot set ordering multiple times."
    ):
        collection_client.order_by("created").order_by("name")


def test_url(collection_client) -> None:
    filter_query = RQLQuery(status="active")
    custom_collection = (
        collection_client.filter(filter_query)
        .select("-audit", "product.agreements", "-product.agreements.product")
        .order_by("-created", "name")
    )

    url = custom_collection.build_url()

    assert custom_collection != collection_client
    assert url == (
        "/api/v1/test?order=-created,name"
        "&select=-audit,product.agreements,-product.agreements.product"
        "&eq(status,active)"
    )


def test_clone(collection_client) -> None:
    configured = (
        collection_client
        .filter(RQLQuery(status="active"))
        .order_by("created", "-name")
        .select("agreement", "-product")
    )

    cloned = configured.clone(configured)

    assert cloned is not configured
    assert isinstance(cloned, configured.__class__)
    assert cloned.http_client is configured.http_client
    assert str(cloned.query_rql) == str(configured.query_rql)

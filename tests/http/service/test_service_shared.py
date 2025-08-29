import pytest

from mpt_api_client.rql.query_builder import RQLQuery


def test_filter(dummy_service):
    filter_query = RQLQuery(status="active")

    new_collection = dummy_service.filter(filter_query)

    assert dummy_service.query_rql is None
    assert new_collection != dummy_service
    assert new_collection.query_rql == filter_query


def test_multiple_filters(dummy_service) -> None:
    filter_query = RQLQuery(status="active")
    filter_query2 = RQLQuery(name="test")

    new_collection = dummy_service.filter(filter_query).filter(filter_query2)

    assert dummy_service.query_rql is None
    assert new_collection.query_rql == filter_query & filter_query2


def test_select(dummy_service) -> None:
    new_collection = dummy_service.select("agreement", "-product")

    assert dummy_service.query_select is None
    assert new_collection != dummy_service
    assert new_collection.query_select == ["agreement", "-product"]


def test_select_exception(dummy_service) -> None:
    with pytest.raises(ValueError):
        dummy_service.select("agreement").select("product")


def test_order_by(dummy_service):
    new_collection = dummy_service.order_by("created", "-name")

    assert dummy_service.query_order_by is None
    assert new_collection != dummy_service
    assert new_collection.query_order_by == ["created", "-name"]


def test_order_by_exception(dummy_service):
    with pytest.raises(
        ValueError, match=r"Ordering is already set. Cannot set ordering multiple times."
    ):
        dummy_service.order_by("created").order_by("name")


def test_url(dummy_service) -> None:
    filter_query = RQLQuery(status="active")
    custom_collection = (
        dummy_service.filter(filter_query)
        .select("-audit", "product.agreements", "-product.agreements.product")
        .order_by("-created", "name")
    )

    url = custom_collection.build_url()

    assert custom_collection != dummy_service
    assert url == (
        "/api/v1/test?order=-created,name"
        "&select=-audit,product.agreements,-product.agreements.product"
        "&eq(status,active)"
    )


def test_clone(dummy_service) -> None:
    configured = (
        dummy_service.filter(RQLQuery(status="active"))
        .order_by("created", "-name")
        .select("agreement", "-product")
    )

    cloned = configured.clone()

    assert cloned is not configured
    assert isinstance(cloned, configured.__class__)
    assert cloned.http_client is configured.http_client
    assert str(cloned.query_rql) == str(configured.query_rql)

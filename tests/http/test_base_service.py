import pytest

from mpt_api_client import RQLQuery
from mpt_api_client.http import Service
from tests.conftest import DummyModel


class EndpointDummyService(Service[DummyModel]):
    _endpoint = "/api/{version}/test"
    _model_class = DummyModel


@pytest.fixture
def base_dummy_service(http_client):
    return EndpointDummyService(http_client=http_client, endpoint_params={"version": "v1"})


def test_endpoint(http_client):
    service = EndpointDummyService(http_client=http_client, endpoint_params={"version": "vLatest"})

    assert service.endpoint_params == {"version": "vLatest"}
    assert service.endpoint == "/api/vLatest/test"


def test_filter(base_dummy_service, filter_status_active):
    new_collection = base_dummy_service.filter(filter_status_active)

    assert base_dummy_service.query_rql is None
    assert new_collection != base_dummy_service
    assert new_collection.query_rql == filter_status_active


def test_multiple_filters(base_dummy_service) -> None:
    filter_query = RQLQuery(status="active")
    filter_query2 = RQLQuery(name="test")

    new_collection = base_dummy_service.filter(filter_query).filter(filter_query2)

    assert base_dummy_service.query_rql is None
    assert new_collection.query_rql == filter_query & filter_query2


def test_select(base_dummy_service) -> None:
    new_collection = base_dummy_service.select("agreement", "-product")

    assert base_dummy_service.query_select is None
    assert new_collection != base_dummy_service
    assert new_collection.query_select == ["agreement", "-product"]


def test_select_exception(base_dummy_service) -> None:
    with pytest.raises(ValueError):
        base_dummy_service.select("agreement").select("product")


def test_order_by(base_dummy_service):
    new_collection = base_dummy_service.order_by("created", "-name")

    assert base_dummy_service.query_order_by is None
    assert new_collection != base_dummy_service
    assert new_collection.query_order_by == ["created", "-name"]


def test_order_by_exception(base_dummy_service):
    with pytest.raises(
        ValueError, match=r"Ordering is already set. Cannot set ordering multiple times."
    ):
        base_dummy_service.order_by("created").order_by("name")


def test_url(base_dummy_service, filter_status_active) -> None:
    custom_collection = (
        base_dummy_service.filter(filter_status_active)
        .select("-audit", "product.agreements", "-product.agreements.product")
        .order_by("-created", "name")
    )

    url = custom_collection.build_url()

    assert custom_collection != base_dummy_service
    assert url == (
        "/api/v1/test?order=-created,name"
        "&select=-audit,product.agreements,-product.agreements.product"
        "&eq(status,active)"
    )


def test_clone(base_dummy_service, filter_status_active) -> None:
    configured = (
        base_dummy_service.filter(filter_status_active)
        .order_by("created", "-name")
        .select("agreement", "-product")
    )

    cloned = configured.clone()

    assert cloned is not configured
    assert isinstance(cloned, configured.__class__)
    assert cloned.http_client is configured.http_client
    assert str(cloned.query_rql) == str(configured.query_rql)
    assert cloned.endpoint_params == configured.endpoint_params

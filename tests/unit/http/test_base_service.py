from mpt_api_client.http import Service
from mpt_api_client.http.query_state import QueryState
from tests.unit.conftest import DummyModel
from tests.unit.http.conftest import DummyService


class ParametrisedDummyService(  # noqa: WPS215
    Service[DummyModel],
):
    _endpoint = "/api/{version}/test/{tenant}"
    _model_class = DummyModel


def test_endpoint(http_client):
    result = ParametrisedDummyService(
        http_client=http_client, endpoint_params={"version": "vLatest", "tenant": "T-123"}
    )

    assert result.endpoint_params == {"version": "vLatest", "tenant": "T-123"}
    assert result.path == "/api/vLatest/test/T-123"


def test_endpoint_with_multiple_params(http_client):
    result = ParametrisedDummyService(
        http_client=http_client, endpoint_params={"version": "v2", "tenant": "test-tenant"}
    )

    assert result.path == "/api/v2/test/test-tenant"


def test_build_url_no_query_params(dummy_service):
    result = dummy_service.build_path()

    assert result == "/api/v1/test"


def test_build_url_with_query_params(dummy_service):
    query_params = {"limit": "10", "offset": "20"}

    result = dummy_service.build_path(query_params)

    assert result == "/api/v1/test?limit=10&offset=20"


def test_build_url_with_query_state(http_client, filter_status_active):
    service_with_state = DummyService(
        http_client=http_client,
        query_state=QueryState(
            rql=filter_status_active, order_by=["created", "-name"], select=["id", "name"]
        ),
    )

    result = service_with_state.build_path()

    assert result == "/api/v1/test?order=created,-name&select=id,name&eq(status,active)"


def test_build_url_with_query_state_and_params(http_client, filter_status_active):
    service_with_state = ParametrisedDummyService(
        http_client=http_client,
        query_state=QueryState(rql=filter_status_active),
        endpoint_params={"version": "v2", "tenant": "T-123"},
    )
    query_params = {"limit": "5"}

    result = service_with_state.build_path(query_params)

    assert result == "/api/v2/test/T-123?limit=5&eq(status,active)"


def test_build_url_with_chained_methods(dummy_service, filter_status_active):
    chained_service = (
        dummy_service
        .filter(filter_status_active)
        .order_by("-created", "name")
        .select("id", "name", "-audit")
    )

    result = chained_service.build_path({"limit": "10"})

    expected_url = (
        "/api/v1/test?limit=10&order=-created,name&select=id,name,-audit&eq(status,active)"
    )
    assert result == expected_url

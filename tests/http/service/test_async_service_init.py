import pytest

from mpt_api_client.rql.query_builder import RQLQuery
from tests.http.conftest import AsyncDummyService


@pytest.fixture
def sample_rql_query():
    return RQLQuery(status="active")


def test_init_defaults(async_dummy_service):
    assert async_dummy_service.query_rql is None
    assert async_dummy_service.query_order_by is None
    assert async_dummy_service.query_select is None
    assert async_dummy_service.build_url() == "/api/v1/test"


def test_init_with_filter(async_http_client, sample_rql_query):
    collection_client = AsyncDummyService(
        http_client=async_http_client,
        query_rql=sample_rql_query,
    )

    assert collection_client.query_rql == sample_rql_query
    assert collection_client.query_order_by is None
    assert collection_client.query_select is None
    assert collection_client.build_url() == "/api/v1/test?eq(status,active)"

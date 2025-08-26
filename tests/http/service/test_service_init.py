import pytest

from mpt_api_client.rql.query_builder import RQLQuery
from tests.http.conftest import DummyService


@pytest.fixture
def sample_rql_query():
    return RQLQuery(status="active")


def test_init_defaults(http_client):
    collection_client = DummyService(http_client=http_client)

    assert collection_client.query_rql is None
    assert collection_client.query_order_by is None
    assert collection_client.query_select is None
    assert collection_client.build_url() == "/api/v1/test"


def test_init_with_filter(http_client, sample_rql_query):
    collection_client = DummyService(
        http_client=http_client,
        query_rql=sample_rql_query,
    )

    assert collection_client.query_rql == sample_rql_query
    assert collection_client.query_order_by is None
    assert collection_client.query_select is None
    assert collection_client.build_url() == "/api/v1/test?eq(status,active)"

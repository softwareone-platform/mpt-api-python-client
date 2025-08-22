import pytest

from mpt_api_client.http.client import HTTPClient
from mpt_api_client.rql.query_builder import RQLQuery
from tests.http.conftest import DummyCollectionClient


@pytest.fixture
def mock_mpt_client(api_url, api_token):
    return HTTPClient(base_url=api_url, api_token=api_token)


@pytest.fixture
def sample_rql_query():
    return RQLQuery(status="active")


def test_init_defaults(http_client):
    collection_client = DummyCollectionClient(client=http_client)

    assert collection_client.query_rql is None
    assert collection_client.query_order_by is None
    assert collection_client.query_select is None
    assert collection_client.build_url() == "/api/v1/test"


def test_init_with_filter(http_client, sample_rql_query):
    collection_client = DummyCollectionClient(
        client=http_client,
        query_rql=sample_rql_query,
    )

    assert collection_client.query_rql == sample_rql_query
    assert collection_client.query_order_by is None
    assert collection_client.query_select is None
    assert collection_client.build_url() == "/api/v1/test?eq(status,active)"

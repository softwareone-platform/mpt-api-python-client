import pytest

from mpt_api_client.resources.catalog.product_terms import (
    AsyncTermService,
    TermService,
)


@pytest.fixture
def term_service(http_client):
    return TermService(http_client=http_client, endpoint_params={"product_id": "PRD-001"})


@pytest.fixture
def async_term_service(async_http_client):
    return AsyncTermService(
        http_client=async_http_client, endpoint_params={"product_id": "PRD-001"}
    )


def test_endpoint(term_service):
    assert term_service.endpoint == "/public/v1/catalog/products/PRD-001/terms"


def test_async_endpoint(async_term_service):
    assert async_term_service.endpoint == "/public/v1/catalog/products/PRD-001/terms"


@pytest.mark.parametrize(
    "method", ["get", "create", "delete", "update", "review", "publish", "unpublish"]
)
def test_methods_present(term_service, method):
    assert hasattr(term_service, method)


@pytest.mark.parametrize(
    "method", ["get", "create", "delete", "update", "review", "publish", "unpublish"]
)
def test_async_methods_present(async_term_service, method):
    assert hasattr(async_term_service, method)

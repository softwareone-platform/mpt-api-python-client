import pytest

from mpt_api_client.resources.commerce.requests import AsyncRequestService, RequestService


@pytest.fixture
def request_service(http_client):
    return RequestService(http_client=http_client)


@pytest.fixture
def async_request_service(http_client):
    return AsyncRequestService(http_client=http_client)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "validate", "process", "query", "complete", "template"],
)
def test_mixins_present(request_service, method):
    assert hasattr(request_service, method)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "validate", "process", "query", "complete", "template"],
)
def test_async_mixins_present(async_request_service, method):
    assert hasattr(async_request_service, method)

import pytest

from mpt_api_client.resources.billing.statements import AsyncStatementsService, StatementsService


@pytest.fixture
def statements_service(http_client):
    return StatementsService(http_client=http_client)


@pytest.fixture
def async_statements_service(async_http_client):
    return AsyncStatementsService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method",
    ["get", "update", "issue", "cancel", "error", "pending", "queue", "retry", "recalculate"],
)
def test_mixins_present(statements_service, method):
    assert hasattr(statements_service, method)


@pytest.mark.parametrize(
    "method",
    ["get", "update", "issue", "cancel", "error", "pending", "queue", "retry", "recalculate"],
)
def test_async_mixins_present(async_statements_service, method):
    assert hasattr(async_statements_service, method)

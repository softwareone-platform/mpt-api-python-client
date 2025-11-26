import pytest

from mpt_api_client.resources.billing.statement_charges import (
    AsyncStatementChargesService,
    StatementChargesService,
)
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
    result = hasattr(statements_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "update", "issue", "cancel", "error", "pending", "queue", "retry", "recalculate"],
)
def test_async_mixins_present(async_statements_service, method):
    result = hasattr(async_statements_service, method)

    assert result is True


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("charges", StatementChargesService),
    ],
)
def test_property_services(statements_service, service_method, expected_service_class):
    result = getattr(statements_service, service_method)("STM-0000-0001")

    assert isinstance(result, expected_service_class)
    assert result.endpoint_params == {"statement_id": "STM-0000-0001"}


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("charges", AsyncStatementChargesService),
    ],
)
def test_async_property_services(async_statements_service, service_method, expected_service_class):
    result = getattr(async_statements_service, service_method)("STM-0000-0001")

    assert isinstance(result, expected_service_class)
    assert result.endpoint_params == {"statement_id": "STM-0000-0001"}

import pytest

from mpt_api_client.resources.billing.statement_charges import (
    AsyncStatementChargesService,
    StatementChargesService,
)


@pytest.fixture
def statement_charges_service(http_client):
    return StatementChargesService(
        http_client=http_client, endpoint_params={"statement_id": "STM-0000-0001"}
    )


@pytest.fixture
def async_statement_charges_service(async_http_client):
    return AsyncStatementChargesService(
        http_client=async_http_client, endpoint_params={"statement_id": "STM-0000-0001"}
    )


def test_endpoint(statement_charges_service):
    assert statement_charges_service.path == ("/public/v1/billing/statements/STM-0000-0001/charges")


def test_async_endpoint(async_statement_charges_service):
    assert async_statement_charges_service.path == (
        "/public/v1/billing/statements/STM-0000-0001/charges"
    )


@pytest.mark.parametrize("method", ["get"])
def test_methods_present(statement_charges_service, method):
    assert hasattr(statement_charges_service, method)


@pytest.mark.parametrize("method", ["get"])
def test_async_methods_present(async_statement_charges_service, method):
    assert hasattr(async_statement_charges_service, method)

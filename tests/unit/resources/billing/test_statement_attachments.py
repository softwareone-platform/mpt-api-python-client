import pytest

from mpt_api_client.resources.billing.statement_attachments import (
    AsyncStatementAttachmentsService,
    StatementAttachmentsService,
)


@pytest.fixture
def statement_attachments_service(http_client) -> StatementAttachmentsService:
    return StatementAttachmentsService(
        http_client=http_client, endpoint_params={"statement_id": "STM-0000-0001"}
    )


@pytest.fixture
def async_statement_attachments_service(async_http_client) -> AsyncStatementAttachmentsService:
    return AsyncStatementAttachmentsService(
        http_client=async_http_client, endpoint_params={"statement_id": "STM-0000-0001"}
    )


def test_endpoint(statement_attachments_service) -> None:
    result = (
        statement_attachments_service.path
        == "/public/v1/billing/statements/STM-0000-0001/attachments"
    )

    assert result is True


def test_async_endpoint(async_statement_attachments_service) -> None:
    result = (
        async_statement_attachments_service.path
        == "/public/v1/billing/statements/STM-0000-0001/attachments"
    )

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate", "download"])
def test_methods_present(statement_attachments_service, method: str) -> None:
    result = hasattr(statement_attachments_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate", "download"])
def test_async_methods_present(async_statement_attachments_service, method: str) -> None:
    result = hasattr(async_statement_attachments_service, method)

    assert result is True

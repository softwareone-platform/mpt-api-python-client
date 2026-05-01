import pytest

from mpt_api_client.resources.billing.statement_attachments import (
    AsyncStatementAttachmentsService,
    StatementAttachment,
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


def test_attachment_inherited_primitive_fields(attachment_data):
    result = StatementAttachment(attachment_data)

    assert result.to_dict() == attachment_data


def test_attachment_inherited_fields_absent():  # noqa: WPS218
    result = StatementAttachment({"id": "ATT-001"})

    assert result.id == "ATT-001"
    assert result.name is None
    assert result.type is None
    assert result.size is None
    assert result.description is None
    assert result.content_type is None

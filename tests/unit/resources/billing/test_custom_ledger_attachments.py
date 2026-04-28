import pytest

from mpt_api_client.resources.billing.custom_ledger_attachments import (
    AsyncCustomLedgerAttachmentsService,
    CustomLedgerAttachment,
    CustomLedgerAttachmentsService,
)


@pytest.fixture
def custom_ledger_attachments_service(http_client):
    return CustomLedgerAttachmentsService(
        http_client=http_client, endpoint_params={"custom_ledger_id": "LDG-0000-0001"}
    )


@pytest.fixture
def async_custom_ledger_attachments_service(async_http_client):
    return AsyncCustomLedgerAttachmentsService(
        http_client=async_http_client, endpoint_params={"custom_ledger_id": "LDG-0000-0001"}
    )


def test_endpoint(custom_ledger_attachments_service):
    result = custom_ledger_attachments_service.path == (
        "/public/v1/billing/custom-ledgers/LDG-0000-0001/attachments"
    )

    assert result is True


def test_async_endpoint(async_custom_ledger_attachments_service):
    result = async_custom_ledger_attachments_service.path == (
        "/public/v1/billing/custom-ledgers/LDG-0000-0001/attachments"
    )

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate", "download"])
def test_methods_present(custom_ledger_attachments_service, method: str):
    result = hasattr(custom_ledger_attachments_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate", "download"])
def test_async_methods_present(async_custom_ledger_attachments_service, method: str):
    result = hasattr(async_custom_ledger_attachments_service, method)

    assert result is True


def test_attachment_inherited_primitive_fields(attachment_data):
    result = CustomLedgerAttachment(attachment_data)

    assert result.to_dict() == attachment_data


def test_attachment_inherited_fields_absent():  # noqa: WPS218
    result = CustomLedgerAttachment({"id": "ATT-001"})

    assert result.id == "ATT-001"
    assert result.name is None
    assert result.type is None
    assert result.size is None
    assert result.description is None
    assert result.content_type is None

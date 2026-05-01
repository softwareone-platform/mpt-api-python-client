import pytest

from mpt_api_client.resources.billing.journal_attachments import (
    AsyncJournalAttachmentsService,
    JournalAttachment,
    JournalAttachmentsService,
)


@pytest.fixture
def journal_attachments_service(http_client) -> JournalAttachmentsService:
    return JournalAttachmentsService(
        http_client=http_client, endpoint_params={"journal_id": "JRN-0000-0001"}
    )


@pytest.fixture
def async_journal_attachments_service(async_http_client) -> AsyncJournalAttachmentsService:
    return AsyncJournalAttachmentsService(
        http_client=async_http_client, endpoint_params={"journal_id": "JRN-0000-0001"}
    )


def test_endpoint(journal_attachments_service) -> None:
    result = (
        journal_attachments_service.path == "/public/v1/billing/journals/JRN-0000-0001/attachments"
    )

    assert result is True


def test_async_endpoint(async_journal_attachments_service) -> None:
    result = (
        async_journal_attachments_service.path
        == "/public/v1/billing/journals/JRN-0000-0001/attachments"
    )

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate", "download"])
def test_methods_present(journal_attachments_service, method: str) -> None:
    result = hasattr(journal_attachments_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate", "download"])
def test_async_methods_present(async_journal_attachments_service, method: str) -> None:
    result = hasattr(async_journal_attachments_service, method)

    assert result is True


def test_attachment_inherited_primitive_fields(attachment_data):
    result = JournalAttachment(attachment_data)

    assert result.to_dict() == attachment_data


def test_attachment_inherited_fields_absent():  # noqa: WPS218
    result = JournalAttachment({"id": "ATT-001"})

    assert result.id == "ATT-001"
    assert result.name is None
    assert result.type is None
    assert result.size is None
    assert result.description is None
    assert result.content_type is None

import pytest

from mpt_api_client.resources.billing.journal_attachments import (
    AsyncJournalAttachmentsService,
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
    assert (
        journal_attachments_service.endpoint
        == "/public/v1/billing/journals/JRN-0000-0001/attachments"
    )


def test_async_endpoint(async_journal_attachments_service) -> None:
    assert (
        async_journal_attachments_service.endpoint
        == "/public/v1/billing/journals/JRN-0000-0001/attachments"
    )


@pytest.mark.parametrize("method", ["get", "create", "update", "delete"])
def test_methods_present(journal_attachments_service, method: str) -> None:
    assert hasattr(journal_attachments_service, method)


@pytest.mark.parametrize("method", ["get", "create", "update", "delete"])
def test_async_methods_present(async_journal_attachments_service, method: str) -> None:
    assert hasattr(async_journal_attachments_service, method)

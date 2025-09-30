import pytest

from mpt_api_client.resources.billing.journal_upload import (
    AsyncJournalUploadService,
    JournalUploadService,
)


@pytest.fixture
def journal_upload_service(http_client):
    return JournalUploadService(
        http_client=http_client, endpoint_params={"journal_id": "JRN-0000-0001"}
    )


@pytest.fixture
def async_journal_upload_service(async_http_client):
    return AsyncJournalUploadService(
        http_client=async_http_client, endpoint_params={"journal_id": "JRN-0000-0001"}
    )


def test_endpoint(journal_upload_service) -> None:
    assert journal_upload_service.endpoint == "/public/v1/billing/journals/JRN-0000-0001/upload"


def test_async_endpoint(async_journal_upload_service) -> None:
    assert (
        async_journal_upload_service.endpoint == "/public/v1/billing/journals/JRN-0000-0001/upload"
    )


@pytest.mark.parametrize("method", ["create"])
def test_methods_present(journal_upload_service, method: str) -> None:
    assert hasattr(journal_upload_service, method)


@pytest.mark.parametrize("method", ["create"])
def test_async_methods_present(async_journal_upload_service, method: str) -> None:
    assert hasattr(async_journal_upload_service, method)

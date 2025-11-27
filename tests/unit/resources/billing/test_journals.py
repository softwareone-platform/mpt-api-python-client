import pytest

from mpt_api_client.resources.billing.journal_attachments import (
    AsyncJournalAttachmentsService,
    JournalAttachmentsService,
)
from mpt_api_client.resources.billing.journal_charges import (
    AsyncJournalChargesService,
    JournalChargesService,
)
from mpt_api_client.resources.billing.journal_sellers import (
    AsyncJournalSellersService,
    JournalSellersService,
)
from mpt_api_client.resources.billing.journal_upload import (
    AsyncJournalUploadService,
    JournalUploadService,
)
from mpt_api_client.resources.billing.journals import AsyncJournalsService, JournalsService


@pytest.fixture
def journals_service(http_client):
    return JournalsService(http_client=http_client)


@pytest.fixture
def async_journals_service(async_http_client):
    return AsyncJournalsService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "regenerate", "submit", "enquiry", "accept"],
)
def test_mixins_present(journals_service, method):
    result = hasattr(journals_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "regenerate", "submit", "enquiry", "accept"],
)
def test_async_mixins_present(async_journals_service, method):
    result = hasattr(async_journals_service, method)

    assert result is True


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("attachments", JournalAttachmentsService),
        ("sellers", JournalSellersService),
        ("charges", JournalChargesService),
        ("upload", JournalUploadService),
    ],
)
def test_property_services(journals_service, service_method, expected_service_class):
    result = getattr(journals_service, service_method)("JRN-0000-0001")

    assert isinstance(result, expected_service_class)
    assert result.endpoint_params == {"journal_id": "JRN-0000-0001"}


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("attachments", AsyncJournalAttachmentsService),
        ("sellers", AsyncJournalSellersService),
        ("charges", AsyncJournalChargesService),
        ("upload", AsyncJournalUploadService),
    ],
)
def test_async_property_services(async_journals_service, service_method, expected_service_class):
    result = getattr(async_journals_service, service_method)("JRN-0000-0001")

    assert isinstance(result, expected_service_class)
    assert result.endpoint_params == {"journal_id": "JRN-0000-0001"}

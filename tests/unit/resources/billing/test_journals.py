import httpx
import pytest
import respx

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
from mpt_api_client.resources.billing.journals import AsyncJournalsService, JournalsService


@pytest.fixture
def journals_service(http_client):
    return JournalsService(http_client=http_client)


@pytest.fixture
def async_journals_service(async_http_client):
    return AsyncJournalsService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "regenerate", "submit", "enquiry", "accept", "upload"],
)
def test_mixins_present(journals_service, method):
    result = hasattr(journals_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "regenerate", "submit", "enquiry", "accept", "upload"],
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
    ],
)
def test_async_property_services(async_journals_service, service_method, expected_service_class):
    result = getattr(async_journals_service, service_method)("JRN-0000-0001")

    assert isinstance(result, expected_service_class)
    assert result.endpoint_params == {"journal_id": "JRN-0000-0001"}


def test_upload(journals_service, tmp_path) -> None:
    file_path = tmp_path / "journal.jsonl"
    file_path.write_text("test data")
    with file_path.open("rb") as file_obj, respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/billing/journals/JRN-0000-0001/upload"
        ).mock(return_value=httpx.Response(200, json={"result": "ok"}))

        result = journals_service.upload(
            journal_id="JRN-0000-0001",
            file=file_obj,
        )

        assert mock_route.called
        assert result is not None


async def test_async_upload(async_journals_service, tmp_path) -> None:
    file_path = tmp_path / "journal.jsonl"
    file_path.write_text("test data")
    with file_path.open("rb") as file_obj, respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/billing/journals/JRN-0000-0001/upload"
        ).mock(return_value=httpx.Response(200, json={"result": "ok"}))

        result = await async_journals_service.upload(
            journal_id="JRN-0000-0001",
            file=file_obj,
        )

        assert mock_route.called
        assert result is not None


def test_upload_without_file(journals_service) -> None:
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/billing/journals/JRN-0000-0001/upload"
        ).mock(return_value=httpx.Response(200, json={"result": "ok"}))

        result = journals_service.upload(
            journal_id="JRN-0000-0001",
            file=None,
        )

        assert mock_route.called
        assert result is not None


async def test_async_upload_without_file(async_journals_service) -> None:
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/billing/journals/JRN-0000-0001/upload"
        ).mock(return_value=httpx.Response(200, json={"result": "ok"}))

        result = await async_journals_service.upload(
            journal_id="JRN-0000-0001",
            file=None,
        )

        assert mock_route.called
        assert result is not None

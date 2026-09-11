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

JOURNAL_ID = "JRN-0000-0001"
UPLOAD_URL = "https://api.example.com/public/v1/billing/journals/JRN-0000-0001/upload"
FILE_PART_AS_NDJSON = 'filename="journal.jsonl"\r\nContent-Type: application/x-ndjson'
FILE_PART_AS_JSONL = 'filename="journal.jsonl"\r\nContent-Type: application/jsonl'
ID_PART_AS_FORM_FIELD = f'form-data; name="id"\r\n\r\n{JOURNAL_ID}'


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


def mock_upload_route():
    upload_response = httpx.Response(200, json={"result": "ok"})
    return respx.post(UPLOAD_URL).mock(return_value=upload_response)


def request_body(mock_route):
    request = mock_route.calls[0].request
    return request.content.decode()


@pytest.fixture
def journal_file(tmp_path):
    file_path = tmp_path / "journal.jsonl"
    file_path.write_bytes(b'{"id": 1}\n')
    return file_path


def test_upload(journals_service, journal_file):
    with journal_file.open("rb") as file_obj, respx.mock:
        mock_route = mock_upload_route()

        result = journals_service.upload(journal_id=JOURNAL_ID, file=file_obj)

        assert mock_route.called
        assert result is not None


async def test_async_upload(async_journals_service, journal_file):
    with journal_file.open("rb") as file_obj, respx.mock:
        mock_route = mock_upload_route()

        result = await async_journals_service.upload(journal_id=JOURNAL_ID, file=file_obj)

        assert mock_route.called
        assert result is not None


def test_upload_without_file(journals_service):
    with respx.mock:
        mock_route = mock_upload_route()

        result = journals_service.upload(journal_id=JOURNAL_ID, file=None)

        assert mock_route.called
        assert result is not None


async def test_async_upload_without_file(async_journals_service):
    with respx.mock:
        mock_route = mock_upload_route()

        result = await async_journals_service.upload(journal_id=JOURNAL_ID, file=None)

        assert mock_route.called
        assert result is not None


def test_upload_declares_ndjson_type(journals_service, journal_file):
    with journal_file.open("rb") as file_obj, respx.mock:
        mock_route = mock_upload_route()

        journals_service.upload(journal_id=JOURNAL_ID, file=file_obj)  # act

        assert FILE_PART_AS_NDJSON in request_body(mock_route)


async def test_async_upload_declares_ndjson_type(async_journals_service, journal_file):
    with journal_file.open("rb") as file_obj, respx.mock:
        mock_route = mock_upload_route()

        await async_journals_service.upload(journal_id=JOURNAL_ID, file=file_obj)  # act

        assert FILE_PART_AS_NDJSON in request_body(mock_route)


def test_upload_keeps_caller_content_type(journals_service, journal_file):
    with journal_file.open("rb") as file_obj, respx.mock:
        mock_route = mock_upload_route()

        journals_service.upload(
            journal_id=JOURNAL_ID,
            file=("journal.jsonl", file_obj, "application/jsonl"),
        )  # act

        assert FILE_PART_AS_JSONL in request_body(mock_route)


def test_upload_sends_id_form_field(journals_service, journal_file):
    with journal_file.open("rb") as file_obj, respx.mock:
        mock_route = mock_upload_route()

        journals_service.upload(journal_id=JOURNAL_ID, file=file_obj)  # act

        assert ID_PART_AS_FORM_FIELD in request_body(mock_route)


async def test_async_upload_sends_id_form_field(async_journals_service, journal_file):
    with journal_file.open("rb") as file_obj, respx.mock:
        mock_route = mock_upload_route()

        await async_journals_service.upload(journal_id=JOURNAL_ID, file=file_obj)  # act

        assert ID_PART_AS_FORM_FIELD in request_body(mock_route)

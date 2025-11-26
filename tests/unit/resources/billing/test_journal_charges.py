import pytest

from mpt_api_client.resources.billing.journal_charges import (
    AsyncJournalChargesService,
    JournalChargesService,
)


@pytest.fixture
def journal_charges_service(http_client):
    return JournalChargesService(
        http_client=http_client, endpoint_params={"journal_id": "JRN-0000-0001"}
    )


@pytest.fixture
def async_journal_charges_service(async_http_client):
    return AsyncJournalChargesService(
        http_client=async_http_client, endpoint_params={"journal_id": "JRN-0000-0001"}
    )


def test_endpoint(journal_charges_service):
    result = journal_charges_service.path == "/public/v1/billing/journals/JRN-0000-0001/charges"

    assert result is True


def test_async_endpoint(async_journal_charges_service):
    result = async_journal_charges_service.path == (
        "/public/v1/billing/journals/JRN-0000-0001/charges"
    )

    assert result is True


@pytest.mark.parametrize("method", ["get"])
def test_methods_present(journal_charges_service, method):
    result = hasattr(journal_charges_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get"])
def test_async_methods_present(async_journal_charges_service, method):
    result = hasattr(async_journal_charges_service, method)

    assert result is True

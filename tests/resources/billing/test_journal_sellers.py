import pytest

from mpt_api_client.resources.billing.journal_sellers import (
    AsyncJournalSellersService,
    JournalSellersService,
)


@pytest.fixture
def journal_sellers_service(http_client):
    return JournalSellersService(
        http_client=http_client, endpoint_params={"journal_id": "JRN-0000-0001"}
    )


@pytest.fixture
def async_journal_sellers_service(async_http_client):
    return AsyncJournalSellersService(
        http_client=async_http_client, endpoint_params={"journal_id": "JRN-0000-0001"}
    )


def test_endpoint(journal_sellers_service):
    assert journal_sellers_service.endpoint == "/public/v1/billing/journals/JRN-0000-0001/sellers"


def test_async_endpoint(async_journal_sellers_service):
    assert (
        async_journal_sellers_service.endpoint
        == "/public/v1/billing/journals/JRN-0000-0001/sellers"
    )


@pytest.mark.parametrize("method", ["get"])
def test_methods_present(journal_sellers_service, method):
    assert hasattr(journal_sellers_service, method)


@pytest.mark.parametrize("method", ["get"])
def test_async_methods_present(async_journal_sellers_service, method):
    assert hasattr(async_journal_sellers_service, method)

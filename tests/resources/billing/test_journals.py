import pytest

from mpt_api_client.resources.billing.journals import AsyncJournalsService, JournalsService


@pytest.fixture
def journals_service(http_client):
    return JournalsService(http_client=http_client)


@pytest.fixture
def async_journals_service(async_http_client):
    return AsyncJournalsService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete"],
)
def test_mixins_present(journals_service, method):
    assert hasattr(journals_service, method)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete"],
)
def test_async_mixins_present(async_journals_service, method):
    assert hasattr(async_journals_service, method)

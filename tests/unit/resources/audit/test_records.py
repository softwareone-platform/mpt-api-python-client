import pytest

from mpt_api_client.resources.audit.records import AsyncRecordsService, RecordsService


@pytest.fixture
def records_service(http_client):
    return RecordsService(http_client=http_client)


@pytest.fixture
def async_records_service(async_http_client):
    return AsyncRecordsService(http_client=async_http_client)


@pytest.mark.parametrize("method", ["get", "create"])
def test_mixins_present(records_service, method):
    result = hasattr(records_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create"])
def test_async_mixins_present(async_records_service, method):
    result = hasattr(async_records_service, method)

    assert result is True

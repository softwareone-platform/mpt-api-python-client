import pytest

from mpt_api_client.resources.audit.audit import AsyncAudit, Audit
from mpt_api_client.resources.audit.event_types import AsyncEventTypesService, EventTypesService
from mpt_api_client.resources.audit.records import AsyncRecordsService, RecordsService


@pytest.fixture
def audit(http_client):
    return Audit(http_client=http_client)


@pytest.fixture
def async_audit(async_http_client):
    return AsyncAudit(http_client=async_http_client)


@pytest.mark.parametrize(
    ("property_name", "expected_service_class"),
    [
        ("records", RecordsService),
        ("event_types", EventTypesService),
    ],
)
def test_audit_properties(audit, property_name, expected_service_class):
    result = getattr(audit, property_name)

    assert isinstance(result, expected_service_class)
    assert result.http_client is audit.http_client


@pytest.mark.parametrize(
    ("property_name", "expected_service_class"),
    [
        ("records", AsyncRecordsService),
        ("event_types", AsyncEventTypesService),
    ],
)
def test_async_audit_properties(async_audit, property_name, expected_service_class):
    result = getattr(async_audit, property_name)

    assert isinstance(result, expected_service_class)
    assert result.http_client is async_audit.http_client


def test_audit_initialization(http_client):
    result = Audit(http_client=http_client)

    assert result.http_client is http_client
    assert isinstance(result, Audit)


def test_async_audit_initialization(async_http_client):
    result = AsyncAudit(http_client=async_http_client)

    assert result.http_client is async_http_client
    assert isinstance(result, AsyncAudit)

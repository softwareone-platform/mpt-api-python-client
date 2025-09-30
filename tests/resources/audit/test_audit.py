import pytest

from mpt_api_client.resources.audit.audit import AsyncAudit, Audit
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
    ],
)
def test_audit_properties(audit, property_name, expected_service_class):
    """Test that Audit properties return correct instances."""
    service = getattr(audit, property_name)

    assert isinstance(service, expected_service_class)
    assert service.http_client is audit.http_client


@pytest.mark.parametrize(
    ("property_name", "expected_service_class"),
    [
        ("records", AsyncRecordsService),
    ],
)
def test_async_audit_properties(async_audit, property_name, expected_service_class):
    """Test that AsyncAudit properties return correct instances."""
    service = getattr(async_audit, property_name)

    assert isinstance(service, expected_service_class)
    assert service.http_client is async_audit.http_client


def test_audit_initialization(http_client):
    audit = Audit(http_client=http_client)

    assert audit.http_client is http_client
    assert isinstance(audit, Audit)


def test_async_audit_initialization(async_http_client):
    async_audit = AsyncAudit(http_client=async_http_client)

    assert async_audit.http_client is async_http_client
    assert isinstance(async_audit, AsyncAudit)

import pytest

from mpt_api_client.resources.billing.credit_memo_attachments import (
    AsyncCreditMemoAttachmentsService,
    CreditMemoAttachmentsService,
)
from mpt_api_client.resources.billing.credit_memos import (
    AsyncCreditMemosService,
    CreditMemosService,
)


@pytest.fixture
def credit_memos_service(http_client):
    return CreditMemosService(http_client=http_client)


@pytest.fixture
def async_credit_memos_service(async_http_client):
    return AsyncCreditMemosService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update"],
)
def test_mixins_present(credit_memos_service, method):
    assert hasattr(credit_memos_service, method)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update"],
)
def test_async_mixins_present(async_credit_memos_service, method):
    assert hasattr(async_credit_memos_service, method)


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("attachments", CreditMemoAttachmentsService),
    ],
)
def test_property_services(credit_memos_service, service_method, expected_service_class):
    service = getattr(credit_memos_service, service_method)("CRM-0000-0001")

    assert isinstance(service, expected_service_class)
    assert service.endpoint_params == {"credit_memo_id": "CRM-0000-0001"}


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("attachments", AsyncCreditMemoAttachmentsService),
    ],
)
def test_async_property_services(
    async_credit_memos_service, service_method, expected_service_class
):
    service = getattr(async_credit_memos_service, service_method)("CRM-0000-0001")

    assert isinstance(service, expected_service_class)
    assert service.endpoint_params == {"credit_memo_id": "CRM-0000-0001"}

import pytest

from mpt_api_client.resources.billing.credit_memo_attachments import (
    AsyncCreditMemoAttachmentsService,
    CreditMemoAttachmentsService,
)


@pytest.fixture
def credit_memo_attachments_service(http_client):
    return CreditMemoAttachmentsService(
        http_client=http_client, endpoint_params={"credit_memo_id": "CRM-0000-0001"}
    )


@pytest.fixture
def async_credit_memo_attachments_service(async_http_client):
    return AsyncCreditMemoAttachmentsService(
        http_client=async_http_client, endpoint_params={"credit_memo_id": "CRM-0000-0001"}
    )


def test_endpoint(credit_memo_attachments_service):
    assert (
        credit_memo_attachments_service.path
        == "/public/v1/billing/credit-memos/CRM-0000-0001/attachments"
    )


def test_async_endpoint(async_credit_memo_attachments_service):
    assert (
        async_credit_memo_attachments_service.path
        == "/public/v1/billing/credit-memos/CRM-0000-0001/attachments"
    )


@pytest.mark.parametrize("method", ["get", "create", "update", "delete"])
def test_methods_present(credit_memo_attachments_service, method: str):
    assert hasattr(credit_memo_attachments_service, method)


@pytest.mark.parametrize("method", ["get", "create", "update", "delete"])
def test_async_methods_present(async_credit_memo_attachments_service, method: str):
    assert hasattr(async_credit_memo_attachments_service, method)

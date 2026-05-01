import pytest

from mpt_api_client.resources.billing.credit_memo_attachments import (
    AsyncCreditMemoAttachmentsService,
    CreditMemoAttachment,
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
    result = (
        credit_memo_attachments_service.path
        == "/public/v1/billing/credit-memos/CRM-0000-0001/attachments"
    )

    assert result is True


def test_async_endpoint(async_credit_memo_attachments_service):
    result = (
        async_credit_memo_attachments_service.path
        == "/public/v1/billing/credit-memos/CRM-0000-0001/attachments"
    )

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate", "download"])
def test_methods_present(credit_memo_attachments_service, method: str):
    result = hasattr(credit_memo_attachments_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate", "download"])
def test_async_methods_present(async_credit_memo_attachments_service, method: str):
    result = hasattr(async_credit_memo_attachments_service, method)

    assert result is True


def test_attachment_inherited_primitive_fields(attachment_data):
    result = CreditMemoAttachment(attachment_data)

    assert result.to_dict() == attachment_data


def test_attachment_inherited_fields_absent():  # noqa: WPS218
    result = CreditMemoAttachment({"id": "ATT-001"})

    assert result.id == "ATT-001"
    assert result.name is None
    assert result.type is None
    assert result.size is None
    assert result.description is None
    assert result.content_type is None

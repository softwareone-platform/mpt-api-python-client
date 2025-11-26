import pytest

from mpt_api_client.resources.commerce.agreements_attachments import (
    AgreementsAttachmentService,
    AsyncAgreementsAttachmentService,
)


@pytest.fixture
def attachment_service(http_client) -> AgreementsAttachmentService:
    return AgreementsAttachmentService(
        http_client=http_client, endpoint_params={"agreement_id": "AGR-123"}
    )


@pytest.fixture
def async_attachment_service(async_http_client) -> AsyncAgreementsAttachmentService:
    return AsyncAgreementsAttachmentService(
        http_client=async_http_client, endpoint_params={"agreement_id": "AGR-123"}
    )


def test_endpoint(attachment_service) -> None:
    result = attachment_service.path == "/public/v1/commerce/agreements/AGR-123/attachments"

    assert result is True


def test_async_endpoint(async_attachment_service) -> None:
    result = async_attachment_service.path == "/public/v1/commerce/agreements/AGR-123/attachments"

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "delete", "download"])
def test_methods_present(attachment_service, method: str) -> None:
    result = hasattr(attachment_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "delete", "download"])
def test_async_methods_present(async_attachment_service, method: str) -> None:
    result = hasattr(async_attachment_service, method)

    assert result is True

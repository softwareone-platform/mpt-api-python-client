import pytest

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.catalog.pricing_policy_attachments import (
    AsyncPricingPolicyAttachmentsService,
    PricingPolicyAttachment,
    PricingPolicyAttachmentsService,
)


@pytest.fixture
def pricing_policy_attachments_service(http_client) -> PricingPolicyAttachmentsService:
    return PricingPolicyAttachmentsService(
        http_client=http_client, endpoint_params={"pricing_policy_id": "PRP-0000-0001"}
    )


@pytest.fixture
def async_pricing_policy_attachments_service(
    async_http_client,
) -> AsyncPricingPolicyAttachmentsService:
    return AsyncPricingPolicyAttachmentsService(
        http_client=async_http_client, endpoint_params={"pricing_policy_id": "PRP-0000-0001"}
    )


@pytest.fixture
def pricing_policy_attachment_data():
    return {
        "id": "ATT-001",
        "name": "Terms of Service",
        "type": "Document",
        "size": 1024,
        "description": "Attachment description",
        "fileName": "terms.pdf",
        "contentType": "application/pdf",
        "status": "Active",
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


def test_endpoint(pricing_policy_attachments_service) -> None:
    result = (
        pricing_policy_attachments_service.path
        == "/public/v1/catalog/pricing-policies/PRP-0000-0001/attachments"
    )

    assert result is True


def test_async_endpoint(async_pricing_policy_attachments_service) -> None:
    result = (
        async_pricing_policy_attachments_service.path
        == "/public/v1/catalog/pricing-policies/PRP-0000-0001/attachments"
    )

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "delete", "update", "download", "iterate"])
def test_methods_present(pricing_policy_attachments_service, method: str) -> None:
    result = hasattr(pricing_policy_attachments_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "delete", "update", "download", "iterate"])
def test_async_methods_present(async_pricing_policy_attachments_service, method: str) -> None:
    result = hasattr(async_pricing_policy_attachments_service, method)

    assert result is True


def test_pricing_policy_attach_primitives(pricing_policy_attachment_data):
    result = PricingPolicyAttachment(pricing_policy_attachment_data)

    assert result.to_dict() == pricing_policy_attachment_data


def test_pricing_policy_attachment_nested_models(pricing_policy_attachment_data):
    result = PricingPolicyAttachment(pricing_policy_attachment_data)

    assert isinstance(result.audit, BaseModel)


def test_pricing_policy_attachment_absent():  # noqa: WPS218
    result = PricingPolicyAttachment({"id": "ATT-001"})

    assert result.id == "ATT-001"
    assert result.name is None
    assert result.type is None
    assert result.size is None
    assert result.description is None
    assert result.content_type is None
    assert result.file_name is None
    assert result.status is None
    assert result.audit is None

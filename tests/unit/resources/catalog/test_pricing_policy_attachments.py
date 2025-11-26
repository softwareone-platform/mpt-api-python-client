import pytest

from mpt_api_client.resources.catalog.pricing_policy_attachments import (
    AsyncPricingPolicyAttachmentsService,
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


@pytest.mark.parametrize(
    "method", ["get", "create", "delete", "update", "download", "activate", "deactivate"]
)
def test_methods_present(pricing_policy_attachments_service, method: str) -> None:
    result = hasattr(pricing_policy_attachments_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method", ["get", "create", "delete", "update", "download", "activate", "deactivate"]
)
def test_async_methods_present(async_pricing_policy_attachments_service, method: str) -> None:
    result = hasattr(async_pricing_policy_attachments_service, method)

    assert result is True

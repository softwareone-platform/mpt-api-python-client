import httpx
import pytest
import respx

from mpt_api_client.resources.catalog.pricing_policies import (
    AsyncPricingPoliciesService,
    PricingPoliciesService,
)
from mpt_api_client.resources.catalog.pricing_policy_attachments import (
    AsyncPricingPolicyAttachmentsService,
    PricingPolicyAttachmentsService,
)


@pytest.fixture
def pricing_policies_service(http_client):
    return PricingPoliciesService(http_client=http_client)


@pytest.fixture
def async_pricing_policies_service(async_http_client):
    return AsyncPricingPoliciesService(http_client=async_http_client)


def test_activate(pricing_policies_service):
    pricing_policy_expected = {
        "id": "PRP-0000-0001",
        "status": "Active",
        "name": "Active Pricing Policy",
    }
    with respx.mock:
        respx.post(
            "https://api.example.com/public/v1/catalog/pricing-policies/PRP-0000-0001/activate"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=pricing_policy_expected,
            )
        )

        result = pricing_policies_service.activate(
            "PRP-0000-0001", {"name": "Active Pricing Policy"}
        )

        assert result.to_dict() == pricing_policy_expected


async def test_async_activate(async_pricing_policies_service):
    pricing_policy_expected = {
        "id": "PRP-0000-0001",
        "status": "Active",
        "name": "Active Pricing Policy",
    }
    with respx.mock:
        respx.post(
            "https://api.example.com/public/v1/catalog/pricing-policies/PRP-0000-0001/activate"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=pricing_policy_expected,
            )
        )

        result = await async_pricing_policies_service.activate(
            "PRP-0000-0001", {"name": "Active Pricing Policy"}
        )

        assert result.to_dict() == pricing_policy_expected


def test_disable(pricing_policies_service):
    pricing_policy_expected = {
        "id": "PRP-0000-0001",
        "status": "Inactive",
        "name": "Inactive Pricing Policy",
    }
    with respx.mock:
        respx.post(
            "https://api.example.com/public/v1/catalog/pricing-policies/PRP-0000-0001/disable"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=pricing_policy_expected,
            )
        )

        result = pricing_policies_service.disable(
            "PRP-0000-0001", {"name": "Inactive Pricing Policy"}
        )

        assert result.to_dict() == pricing_policy_expected


async def test_async_disable(async_pricing_policies_service):
    pricing_policy_expected = {
        "id": "PRP-0000-0001",
        "status": "Inactive",
        "name": "Inactive Pricing Policy",
    }
    with respx.mock:
        respx.post(
            "https://api.example.com/public/v1/catalog/pricing-policies/PRP-0000-0001/disable"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=pricing_policy_expected,
            )
        )

        result = await async_pricing_policies_service.disable(
            "PRP-0000-0001", {"name": "Inactive Pricing Policy"}
        )

        assert result.to_dict() == pricing_policy_expected


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("attachments", PricingPolicyAttachmentsService),
    ],
)
def test_property_services(pricing_policies_service, service_method, expected_service_class):
    result = getattr(pricing_policies_service, service_method)("PRP-0000-0001")

    assert isinstance(result, expected_service_class)
    assert result.endpoint_params == {"pricing_policy_id": "PRP-0000-0001"}


@pytest.mark.parametrize(
    ("service_method", "expected_service_class"),
    [
        ("attachments", AsyncPricingPolicyAttachmentsService),
    ],
)
def test_async_property_services(
    async_pricing_policies_service, service_method, expected_service_class
):
    result = getattr(async_pricing_policies_service, service_method)("PRP-0000-0001")

    assert isinstance(result, expected_service_class)
    assert result.endpoint_params == {"pricing_policy_id": "PRP-0000-0001"}


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "activate", "disable", "iterate"],
)
def test_mixins_present(pricing_policies_service, method):
    result = hasattr(pricing_policies_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "activate", "disable", "iterate"],
)
def test_async_mixins_present(async_pricing_policies_service, method):
    result = hasattr(async_pricing_policies_service, method)

    assert result is True

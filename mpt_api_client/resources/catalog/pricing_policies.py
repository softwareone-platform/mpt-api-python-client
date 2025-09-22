from mpt_api_client.http import (
    AsyncCreateMixin,
    AsyncDeleteMixin,
    AsyncService,
    CreateMixin,
    DeleteMixin,
    Service,
)
from mpt_api_client.models import Model, ResourceData


class PricingPolicy(Model):
    """Pricing policy resource."""


class PricingPoliciesServiceConfig:
    """Pricing policy service config."""

    _endpoint = "/public/v1/catalog/pricing-policies"
    _model_class = PricingPolicy
    _collection_key = "data"


class PricingPoliciesService(  # noqa: WPS215
    CreateMixin[PricingPolicy],
    DeleteMixin,
    Service[PricingPolicy],
    PricingPoliciesServiceConfig,
):
    """Pricing policies service."""

    def activate(self, resource_id: str, resource_data: ResourceData) -> PricingPolicy:
        """Activate pricing policy.

        Args:
            resource_id: Pricing policy resource ID
            resource_data: Pricing policy resource data

        Returns:
            Activated pricing policy.
        """
        return self._resource_action(resource_id, "POST", "activate", json=resource_data)

    def disable(self, resource_id: str, resource_data: ResourceData) -> PricingPolicy:
        """Disable pricing policy.

        Args:
            resource_id: Pricing policy resource ID
            resource_data: Pricing policy resource data

        Returns:
            Disabled pricing policy.
        """
        return self._resource_action(resource_id, "POST", "disable", json=resource_data)


class AsyncPricingPoliciesService(
    AsyncCreateMixin[PricingPolicy],
    AsyncDeleteMixin,
    AsyncService[PricingPolicy],
    PricingPoliciesServiceConfig,
):
    """Async pricing policies service."""

    async def activate(self, resource_id: str, resource_data: ResourceData) -> PricingPolicy:
        """Activate pricing policy.

        Args:
            resource_id: Pricing policy resource ID
            resource_data: Pricing policy resource data

        Returns:
            Activated pricing policy.
        """
        return await self._resource_action(resource_id, "POST", "activate", json=resource_data)

    async def disable(self, resource_id: str, resource_data: ResourceData) -> PricingPolicy:
        """Disable pricing policy.

        Args:
            resource_id: Pricing policy resource ID
            resource_data: Pricing policy resource data

        Returns:
            Disabled pricing policy.
        """
        return await self._resource_action(resource_id, "POST", "disable", json=resource_data)

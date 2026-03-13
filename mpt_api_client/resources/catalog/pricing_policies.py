from mpt_api_client.http import (
    AsyncService,
    Service,
)
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model, ResourceData
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.catalog.pricing_policy_attachments import (
    AsyncPricingPolicyAttachmentsService,
    PricingPolicyAttachmentsService,
)


class PricingPolicy(Model):
    """Pricing policy resource.

    Attributes:
        name: Pricing policy name.
        external_ids: External identifiers for the pricing policy.
        client: Reference to the client account.
        eligibility: Eligibility information.
        markup: Markup percentage.
        margin: Margin percentage.
        notes: Additional notes.
        products: List of associated products.
        status: Pricing policy status.
        statistics: Pricing policy statistics.
        audit: Audit information (created, updated events).
    """

    name: str | None
    external_ids: BaseModel | None
    client: BaseModel | None
    eligibility: BaseModel | None
    markup: float | None
    margin: float | None
    notes: str | None
    products: list[BaseModel] | None
    status: str | None
    statistics: BaseModel | None
    audit: BaseModel | None


class PricingPoliciesServiceConfig:
    """Pricing policy service config."""

    _endpoint = "/public/v1/catalog/pricing-policies"
    _model_class = PricingPolicy
    _collection_key = "data"


class PricingPoliciesService(  # noqa: WPS215
    ManagedResourceMixin[PricingPolicy],
    CollectionMixin[PricingPolicy],
    Service[PricingPolicy],
    PricingPoliciesServiceConfig,
):
    """Pricing policies service."""

    def attachments(self, pricing_policy_id: str) -> PricingPolicyAttachmentsService:
        """Return pricing policy attachments service."""
        return PricingPolicyAttachmentsService(
            http_client=self.http_client,
            endpoint_params={"pricing_policy_id": pricing_policy_id},
        )

    def activate(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> PricingPolicy:
        """Activate pricing policy.

        Args:
            resource_id: Pricing policy resource ID
            resource_data: Pricing policy resource data

        Returns:
            Activated pricing policy.
        """
        return self._resource_action(resource_id, "POST", "activate", json=resource_data)

    def disable(self, resource_id: str, resource_data: ResourceData | None = None) -> PricingPolicy:
        """Disable pricing policy.

        Args:
            resource_id: Pricing policy resource ID
            resource_data: Pricing policy resource data

        Returns:
            Disabled pricing policy.
        """
        return self._resource_action(resource_id, "POST", "disable", json=resource_data)


class AsyncPricingPoliciesService(
    AsyncManagedResourceMixin[PricingPolicy],
    AsyncCollectionMixin[PricingPolicy],
    AsyncService[PricingPolicy],
    PricingPoliciesServiceConfig,
):
    """Async pricing policies service."""

    def attachments(self, pricing_policy_id: str) -> AsyncPricingPolicyAttachmentsService:
        """Return pricing policy attachments service."""
        return AsyncPricingPolicyAttachmentsService(
            http_client=self.http_client,
            endpoint_params={"pricing_policy_id": pricing_policy_id},
        )

    async def activate(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> PricingPolicy:
        """Activate pricing policy.

        Args:
            resource_id: Pricing policy resource ID
            resource_data: Pricing policy resource data

        Returns:
            Activated pricing policy.
        """
        return await self._resource_action(resource_id, "POST", "activate", json=resource_data)

    async def disable(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> PricingPolicy:
        """Disable pricing policy.

        Args:
            resource_id: Pricing policy resource ID
            resource_data: Pricing policy resource data

        Returns:
            Disabled pricing policy.
        """
        return await self._resource_action(resource_id, "POST", "disable", json=resource_data)

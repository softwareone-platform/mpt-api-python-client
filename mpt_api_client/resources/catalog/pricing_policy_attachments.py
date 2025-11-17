from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncFilesOperationsMixin,
    AsyncModifiableResourceMixin,
    CollectionMixin,
    FilesOperationsMixin,
    ModifiableResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.catalog.mixins import ActivatableMixin, AsyncActivatableMixin


class PricingPolicyAttachment(Model):
    """Pricing Policy Attachment resource."""


class PricingPolicyAttachmentsServiceConfig:
    """Pricing Policy Attachments service configuration."""

    _endpoint = "/public/v1/catalog/pricing-policies/{pricing_policy_id}/attachments"
    _model_class = PricingPolicyAttachment
    _collection_key = "data"


class PricingPolicyAttachmentsService(
    FilesOperationsMixin[PricingPolicyAttachment],
    ActivatableMixin[PricingPolicyAttachment],
    ModifiableResourceMixin[PricingPolicyAttachment],
    CollectionMixin[PricingPolicyAttachment],
    Service[PricingPolicyAttachment],
    PricingPolicyAttachmentsServiceConfig,
):
    """Pricing Policy Attachments service."""


class AsyncPricingPolicyAttachmentsService(
    AsyncFilesOperationsMixin[PricingPolicyAttachment],
    AsyncActivatableMixin[PricingPolicyAttachment],
    AsyncModifiableResourceMixin[PricingPolicyAttachment],
    AsyncCollectionMixin[PricingPolicyAttachment],
    AsyncService[PricingPolicyAttachment],
    PricingPolicyAttachmentsServiceConfig,
):
    """Pricing Policy Attachments service."""

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncDeleteMixin,
    AsyncFileOperationsMixin,
    AsyncGetMixin,
    AsyncUpdateMixin,
    DeleteMixin,
    FileOperationsMixin,
    GetMixin,
    UpdateMixin,
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
    FileOperationsMixin[PricingPolicyAttachment],
    DeleteMixin,
    GetMixin[PricingPolicyAttachment],
    UpdateMixin[PricingPolicyAttachment],
    ActivatableMixin[PricingPolicyAttachment],
    Service[PricingPolicyAttachment],
    PricingPolicyAttachmentsServiceConfig,
):
    """Pricing Policy Attachments service."""


class AsyncPricingPolicyAttachmentsService(
    AsyncFileOperationsMixin[PricingPolicyAttachment],
    AsyncDeleteMixin,
    AsyncGetMixin[PricingPolicyAttachment],
    AsyncUpdateMixin[PricingPolicyAttachment],
    AsyncActivatableMixin[PricingPolicyAttachment],
    AsyncService[PricingPolicyAttachment],
    PricingPolicyAttachmentsServiceConfig,
):
    """Pricing Policy Attachments service."""

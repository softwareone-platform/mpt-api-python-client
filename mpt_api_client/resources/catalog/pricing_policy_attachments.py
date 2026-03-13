from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateFileMixin,
    AsyncDownloadFileMixin,
    AsyncModifiableResourceMixin,
    CollectionMixin,
    CreateFileMixin,
    DownloadFileMixin,
    ModifiableResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel


class PricingPolicyAttachment(Model):
    """Pricing Policy Attachment resource.

    Attributes:
        name: Attachment name.
        type: Attachment type.
        size: File size in bytes.
        description: Attachment description.
        file_name: Original file name.
        content_type: MIME content type of the attachment.
        status: Attachment status.
        audit: Audit information (created, updated events).
    """

    name: str | None
    type: str | None
    size: int | None
    description: str | None
    file_name: str | None
    content_type: str | None
    status: str | None
    audit: BaseModel | None


class PricingPolicyAttachmentsServiceConfig:
    """Pricing Policy Attachments service configuration."""

    _endpoint = "/public/v1/catalog/pricing-policies/{pricing_policy_id}/attachments"
    _model_class = PricingPolicyAttachment
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "attachment"


class PricingPolicyAttachmentsService(
    CreateFileMixin[PricingPolicyAttachment],
    DownloadFileMixin[PricingPolicyAttachment],
    ModifiableResourceMixin[PricingPolicyAttachment],
    CollectionMixin[PricingPolicyAttachment],
    Service[PricingPolicyAttachment],
    PricingPolicyAttachmentsServiceConfig,
):
    """Pricing Policy Attachments service."""


class AsyncPricingPolicyAttachmentsService(
    AsyncCreateFileMixin[PricingPolicyAttachment],
    AsyncDownloadFileMixin[PricingPolicyAttachment],
    AsyncModifiableResourceMixin[PricingPolicyAttachment],
    AsyncCollectionMixin[PricingPolicyAttachment],
    AsyncService[PricingPolicyAttachment],
    PricingPolicyAttachmentsServiceConfig,
):
    """Pricing Policy Attachments service."""

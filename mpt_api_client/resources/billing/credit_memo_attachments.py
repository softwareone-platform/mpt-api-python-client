from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    CollectionMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.billing.mixins import AsyncAttachmentMixin, AttachmentMixin


class CreditMemoAttachment(Model):
    """Credit Memo Attachment resource."""


class CreditMemoAttachmentsServiceConfig:
    """Credit Memo Attachments service configuration."""

    _endpoint = "/public/v1/billing/credit-memos/{credit_memo_id}/attachments"
    _model_class = CreditMemoAttachment
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "attachment"


class CreditMemoAttachmentsService(
    AttachmentMixin[CreditMemoAttachment],
    CollectionMixin[CreditMemoAttachment],
    Service[CreditMemoAttachment],
    CreditMemoAttachmentsServiceConfig,
):
    """Credit Memo Attachments service."""


class AsyncCreditMemoAttachmentsService(
    AsyncAttachmentMixin[CreditMemoAttachment],
    AsyncCollectionMixin[CreditMemoAttachment],
    AsyncService[CreditMemoAttachment],
    CreditMemoAttachmentsServiceConfig,
):
    """Credit Memo Attachments service."""

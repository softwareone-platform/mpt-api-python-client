from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncFileOperationsMixin,
    AsyncModifiableResourceMixin,
    CollectionMixin,
    FileOperationsMixin,
    ModifiableResourceMixin,
)
from mpt_api_client.models import Model


class CreditMemoAttachment(Model):
    """Credit Memo Attachment resource."""


class CreditMemoAttachmentsServiceConfig:
    """Credit Memo Attachments service configuration."""

    _endpoint = "/public/v1/billing/credit-memos/{credit_memo_id}/attachments"
    _model_class = CreditMemoAttachment
    _collection_key = "data"


class CreditMemoAttachmentsService(
    FileOperationsMixin[CreditMemoAttachment],
    ModifiableResourceMixin[CreditMemoAttachment],
    CollectionMixin[CreditMemoAttachment],
    Service[CreditMemoAttachment],
    CreditMemoAttachmentsServiceConfig,
):
    """Credit Memo Attachments service."""


class AsyncCreditMemoAttachmentsService(
    AsyncFileOperationsMixin[CreditMemoAttachment],
    AsyncModifiableResourceMixin[CreditMemoAttachment],
    AsyncCollectionMixin[CreditMemoAttachment],
    AsyncService[CreditMemoAttachment],
    CreditMemoAttachmentsServiceConfig,
):
    """Credit Memo Attachments service."""

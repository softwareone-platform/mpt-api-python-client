from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    CollectionMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.billing.mixins import AsyncAttachmentMixin, AttachmentMixin


class StatementAttachment(Model):
    """Statement Attachment resource."""


class StatementAttachmentsServiceConfig:
    """Statement Attachments service configuration."""

    _endpoint = "/public/v1/billing/statements/{statement_id}/attachments"
    _model_class = StatementAttachment
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "attachment"


class StatementAttachmentsService(
    AttachmentMixin[StatementAttachment],
    CollectionMixin[StatementAttachment],
    Service[StatementAttachment],
    StatementAttachmentsServiceConfig,
):
    """Statement Attachments service."""


class AsyncStatementAttachmentsService(
    AsyncAttachmentMixin[StatementAttachment],
    AsyncCollectionMixin[StatementAttachment],
    AsyncService[StatementAttachment],
    StatementAttachmentsServiceConfig,
):
    """Statement Attachments service."""

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    CollectionMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.mixins.attachment_mixin import AsyncAttachmentMixin, AttachmentMixin


class EnrollmentAttachment(Model):
    """Enrollment Attachment resource.

    Attributes:
        name: The name of the attachment.
        description: The description of the attachment.
        type: The type of the attachment.
        filename: The filename of the attachment.
        size: The size of the attachment in bytes.
        content_type: The content type of the attachment.
        enrollment: The enrollment associated with the attachment.
        audit: The audit information for the attachment.
    """

    name: str | None = None
    description: str | None = None
    type: str | None = None
    filename: str | None = None
    size: int | None = None
    content_type: str | None = None
    enrollment: BaseModel | None = None
    audit: BaseModel | None = None


class EnrollmentAttachmentsServiceConfig:
    """Enrollment Attachments service configuration."""

    _endpoint = "/public/v1/program/enrollments/{enrollment_id}/attachments"
    _model_class = EnrollmentAttachment
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "attachment"


class EnrollmentAttachmentsService(
    AttachmentMixin[EnrollmentAttachment],
    CollectionMixin[EnrollmentAttachment],
    Service[EnrollmentAttachment],
    EnrollmentAttachmentsServiceConfig,
):
    """Enrollment Attachments service."""


class AsyncEnrollmentAttachmentsService(
    AsyncAttachmentMixin[EnrollmentAttachment],
    AsyncCollectionMixin[EnrollmentAttachment],
    AsyncService[EnrollmentAttachment],
    EnrollmentAttachmentsServiceConfig,
):
    """Enrollment Attachments service."""

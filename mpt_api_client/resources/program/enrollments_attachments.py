from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    CollectionMixin,
)
from mpt_api_client.models import AttachmentModel
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.mixins.attachment_mixin import AsyncAttachmentMixin, AttachmentMixin


class EnrollmentAttachment(AttachmentModel):
    """Enrollment Attachment resource.

    Attributes:
        filename: The filename of the attachment.
        enrollment: The enrollment associated with the attachment.
        audit: The audit information for the attachment.
    """

    filename: str | None = None
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

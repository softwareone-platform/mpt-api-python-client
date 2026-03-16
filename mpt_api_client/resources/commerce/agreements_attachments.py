from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (  # noqa: WPS235
    AsyncCollectionMixin,
    AsyncCreateFileMixin,
    AsyncDeleteMixin,
    AsyncDownloadFileMixin,
    AsyncGetMixin,
    AsyncUpdateMixin,
    CollectionMixin,
    CreateFileMixin,
    DeleteMixin,
    DownloadFileMixin,
    GetMixin,
    UpdateMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel


class AgreementAttachment(Model):
    """Agreement attachment resource.

    Attributes:
        attachment: Attachment metadata.
        file: File reference or URL.
    """

    attachment: BaseModel | None
    file: str | None  # noqa: WPS110


class AgreementsAttachmentServiceConfig:
    """Orders service config."""

    _endpoint = "/public/v1/commerce/agreements/{agreement_id}/attachments"
    _model_class = AgreementAttachment
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "attachment"


class AgreementsAttachmentService(
    CreateFileMixin[AgreementAttachment],
    UpdateMixin[AgreementAttachment],
    DownloadFileMixin[AgreementAttachment],
    DeleteMixin,
    GetMixin[AgreementAttachment],
    CollectionMixin[AgreementAttachment],
    Service[AgreementAttachment],
    AgreementsAttachmentServiceConfig,
):
    """Attachments service."""


class AsyncAgreementsAttachmentService(
    AsyncCreateFileMixin[AgreementAttachment],
    AsyncUpdateMixin[AgreementAttachment],
    AsyncDownloadFileMixin[AgreementAttachment],
    AsyncDeleteMixin,
    AsyncGetMixin[AgreementAttachment],
    AsyncCollectionMixin[AgreementAttachment],
    AsyncService[AgreementAttachment],
    AgreementsAttachmentServiceConfig,
):
    """Attachments service."""

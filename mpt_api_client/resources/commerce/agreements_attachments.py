from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncDeleteMixin,
    AsyncFilesOperationsMixin,
    AsyncGetMixin,
    CollectionMixin,
    DeleteMixin,
    FilesOperationsMixin,
    GetMixin,
)
from mpt_api_client.models import Model


class AgreementAttachment(Model):
    """Agreement attachment resource."""


class AgreementsAttachmentServiceConfig:
    """Orders service config."""

    _endpoint = "/public/v1/commerce/agreements/{agreement_id}/attachments"
    _model_class = AgreementAttachment
    _collection_key = "data"


class AgreementsAttachmentService(
    FilesOperationsMixin[AgreementAttachment],
    DeleteMixin,
    GetMixin[AgreementAttachment],
    CollectionMixin[AgreementAttachment],
    Service[AgreementAttachment],
    AgreementsAttachmentServiceConfig,
):
    """Attachments service."""


class AsyncAgreementsAttachmentService(
    AsyncFilesOperationsMixin[AgreementAttachment],
    AsyncDeleteMixin,
    AsyncGetMixin[AgreementAttachment],
    AsyncCollectionMixin[AgreementAttachment],
    AsyncService[AgreementAttachment],
    AgreementsAttachmentServiceConfig,
):
    """Attachments service."""

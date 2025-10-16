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
from mpt_api_client.resources.catalog.mixins import AsyncPublishableMixin, PublishableMixin


class Document(Model):
    """Document resource."""


class DocumentServiceConfig:
    """Document service configuration."""

    _endpoint = "/public/v1/catalog/products/{product_id}/documents"
    _model_class = Document
    _collection_key = "data"


class DocumentService(
    FileOperationsMixin[Document],
    DeleteMixin,
    GetMixin[Document],
    UpdateMixin[Document],
    PublishableMixin[Document],
    Service[Document],
    DocumentServiceConfig,
):
    """Document service."""


class AsyncDocumentService(
    AsyncFileOperationsMixin[Document],
    AsyncDeleteMixin,
    AsyncGetMixin[Document],
    AsyncUpdateMixin[Document],
    AsyncPublishableMixin[Document],
    AsyncService[Document],
    DocumentServiceConfig,
):
    """Document service."""

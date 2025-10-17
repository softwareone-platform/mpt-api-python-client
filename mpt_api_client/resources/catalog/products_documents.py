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
    PublishableMixin[Document],
    ModifiableResourceMixin[Document],
    CollectionMixin[Document],
    Service[Document],
    DocumentServiceConfig,
):
    """Document service."""


class AsyncDocumentService(
    AsyncFileOperationsMixin[Document],
    AsyncPublishableMixin[Document],
    AsyncModifiableResourceMixin[Document],
    AsyncCollectionMixin[Document],
    AsyncService[Document],
    DocumentServiceConfig,
):
    """Document service."""

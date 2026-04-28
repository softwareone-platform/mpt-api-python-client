from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncModifiableResourceMixin,
    CollectionMixin,
    ModifiableResourceMixin,
)
from mpt_api_client.models import DocumentModel
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.mixins import (
    AsyncDocumentMixin,
    AsyncReviewableMixin,
    DocumentMixin,
    ReviewableMixin,
)


class Document(DocumentModel):
    """Document resource.

    Attributes:
        language: Language code of the document.
        product: Reference to the product.
        audit: Audit information (created, updated events).
    """

    language: str | None = None
    product: BaseModel | None = None
    audit: BaseModel | None = None


class DocumentServiceConfig:
    """Document service configuration."""

    _endpoint = "/public/v1/catalog/products/{product_id}/documents"
    _model_class = Document
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "document"


class DocumentService(
    DocumentMixin[Document],
    ReviewableMixin[Document],
    ModifiableResourceMixin[Document],
    CollectionMixin[Document],
    Service[Document],
    DocumentServiceConfig,
):
    """Document service."""


class AsyncDocumentService(
    AsyncDocumentMixin[Document],
    AsyncReviewableMixin[Document],
    AsyncModifiableResourceMixin[Document],
    AsyncCollectionMixin[Document],
    AsyncService[Document],
    DocumentServiceConfig,
):
    """Document service."""

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncModifiableResourceMixin,
    CollectionMixin,
    ModifiableResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.mixins import (
    AsyncDocumentMixin,
    AsyncReviewableMixin,
    DocumentMixin,
    ReviewableMixin,
)


class Document(Model):
    """Document resource.

    Attributes:
        name: Document name.
        type: Document type.
        description: Document description.
        status: Document status.
        filename: Original file name.
        size: File size in bytes.
        content_type: MIME content type of the document.
        url: URL to access the document.
        language: Language code of the document.
        product: Reference to the product.
        audit: Audit information (created, updated events).
    """

    name: str | None
    type: str | None
    description: str | None
    status: str | None
    filename: str | None
    size: int | None
    content_type: str | None
    url: str | None
    language: str | None
    product: BaseModel | None
    audit: BaseModel | None


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

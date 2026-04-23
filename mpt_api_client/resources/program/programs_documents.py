from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncModifiableResourceMixin,
    CollectionMixin,
    ModifiableResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.mixins import AsyncDocumentMixin, DocumentMixin


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
        program: Reference to the program.
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
    program: BaseModel | None
    audit: BaseModel | None


class DocumentServiceConfig:
    """Document service configuration."""

    _endpoint = "/public/v1/program/programs/{program_id}/documents"
    _model_class = Document
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "document"


class DocumentService(
    DocumentMixin[Document],
    ModifiableResourceMixin[Document],
    CollectionMixin[Document],
    Service[Document],
    DocumentServiceConfig,
):
    """Program documents service."""


class AsyncDocumentService(
    AsyncDocumentMixin[Document],
    AsyncModifiableResourceMixin[Document],
    AsyncCollectionMixin[Document],
    AsyncService[Document],
    DocumentServiceConfig,
):
    """Async program documents service."""

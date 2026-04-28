from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncModifiableResourceMixin,
    CollectionMixin,
    ModifiableResourceMixin,
)
from mpt_api_client.models import DocumentModel
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.mixins import AsyncDocumentMixin, DocumentMixin


class Document(DocumentModel):
    """Document resource.

    Attributes:
        program: Reference to the program.
        audit: Audit information (created, updated events).
    """

    program: BaseModel | None = None
    audit: BaseModel | None = None


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

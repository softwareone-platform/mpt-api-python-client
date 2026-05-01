from mpt_api_client.models.file_resource_model import FileResourceModel


class DocumentModel(FileResourceModel):
    """Base model for document resources.

    Attributes:
        status: Document status.
        filename: Original file name.
        url: URL to access the document.
    """

    status: str | None = None
    filename: str | None = None
    url: str | None = None

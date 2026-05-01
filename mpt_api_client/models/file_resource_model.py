from mpt_api_client.models.model import Model


class FileResourceModel(Model):
    """Base model for file-like resources (attachments, documents, media, term variants).

    Attributes:
        name: Resource name.
        type: Resource type.
        size: File size in bytes.
        description: Resource description.
        content_type: MIME content type.
    """

    name: str | None = None
    type: str | None = None
    size: int | None = None
    description: str | None = None
    content_type: str | None = None

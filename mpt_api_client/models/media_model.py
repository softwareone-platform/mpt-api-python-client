from mpt_api_client.models.file_resource_model import FileResourceModel


class MediaModel(FileResourceModel):
    """Base model for media resources.

    Attributes:
        status: Media status.
        filename: Original file name.
        display_order: Display order of the media item.
        url: URL to access the media file.
    """

    status: str | None = None
    filename: str | None = None
    display_order: int | None = None
    url: str | None = None

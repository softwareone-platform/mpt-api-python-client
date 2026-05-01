from mpt_api_client.models.file_resource_model import FileResourceModel


class TermVariantModel(FileResourceModel):
    """Base model for term variant resources.

    Attributes:
        asset_url: URL to the variant asset.
        language_code: Language code for this variant.
        status: Variant status.
        filename: Original file name.
        file_id: Identifier of the uploaded file.
    """

    asset_url: str | None = None
    language_code: str | None = None
    status: str | None = None
    filename: str | None = None
    file_id: str | None = None

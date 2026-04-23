from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateFileMixin,
    AsyncModifiableResourceMixin,
    CollectionMixin,
    CreateFileMixin,
    ModifiableResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.mixins import (
    AsyncPublishableMixin,
    PublishableMixin,
)


class ExtensionTermVariant(Model):
    """Extension Term Variant resource.

    Attributes:
        name: Variant name.
        revision: Revision number.
        type: Variant type (Online or File).
        asset_url: URL to the variant asset for Online type.
        language_code: Language code for this variant.
        description: Variant description.
        status: Variant status (Draft, Published, Unpublished, Deleted).
        filename: Original file name for File type.
        size: File size in bytes for File type.
        content_type: MIME content type of the file.
        term: Reference to the parent term.
        file_id: Identifier of the uploaded file.
        audit: Audit information (created, updated, published, unpublished).
    """

    name: str | None
    revision: int | None
    type: str | None
    asset_url: str | None
    language_code: str | None
    description: str | None
    status: str | None
    filename: str | None
    size: int | None
    content_type: str | None
    term: BaseModel | None
    file_id: str | None
    audit: BaseModel | None


class ExtensionTermVariantsServiceConfig:
    """Extension Term Variants service configuration."""

    _endpoint = "/public/v1/integration/extensions/{extension_id}/terms/{term_id}/variants"
    _model_class = ExtensionTermVariant
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "variant"


class ExtensionTermVariantsService(
    PublishableMixin[ExtensionTermVariant],
    CreateFileMixin[ExtensionTermVariant],
    ModifiableResourceMixin[ExtensionTermVariant],
    CollectionMixin[ExtensionTermVariant],
    Service[ExtensionTermVariant],
    ExtensionTermVariantsServiceConfig,
):
    """Sync service for extensions/{extensionId}/terms/{termId}/variants endpoint."""


class AsyncExtensionTermVariantsService(
    AsyncPublishableMixin[ExtensionTermVariant],
    AsyncCreateFileMixin[ExtensionTermVariant],
    AsyncModifiableResourceMixin[ExtensionTermVariant],
    AsyncCollectionMixin[ExtensionTermVariant],
    AsyncService[ExtensionTermVariant],
    ExtensionTermVariantsServiceConfig,
):
    """Async service for extensions/{extensionId}/terms/{termId}/variants endpoint."""

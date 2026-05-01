from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateFileMixin,
    AsyncModifiableResourceMixin,
    CollectionMixin,
    CreateFileMixin,
    ModifiableResourceMixin,
)
from mpt_api_client.models import TermVariantModel
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.mixins import (
    AsyncPublishableMixin,
    PublishableMixin,
)


class ExtensionTermVariant(TermVariantModel):
    """Extension Term Variant resource.

    Attributes:
        revision: Revision number.
        term: Reference to the parent term.
        audit: Audit information (created, updated, published, unpublished).
    """

    revision: int | None = None
    term: BaseModel | None = None
    audit: BaseModel | None = None


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

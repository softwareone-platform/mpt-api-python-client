from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateFileMixin,
    AsyncDeleteMixin,
    AsyncGetMixin,
    AsyncUpdateFileMixin,
    CollectionMixin,
    CreateFileMixin,
    DeleteMixin,
    GetMixin,
    UpdateFileMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.integration.extension_media import (
    AsyncExtensionMediaService,
    ExtensionMediaService,
)
from mpt_api_client.resources.integration.extension_terms import (
    AsyncExtensionTermsService,
    ExtensionTermsService,
)
from mpt_api_client.resources.integration.mixins import (
    AsyncExtensionMixin,
    ExtensionMixin,
)


class Extension(Model):
    """Extension resource.

    Attributes:
        name: Display name of the extension.
        icon: URL or identifier for the extension icon.
        revision: Revision number.
        status: Extension status (Draft, Private, Public, Deleted).
        website: Extension website URL.
        short_description: Short description of the extension.
        long_description: Long description of the extension.
        vendor: Reference to the vendor account.
        categories: Categories assigned to the extension.
        modules: Modules referenced by the extension.
        statistics: Extension usage statistics.
        configuration: Extension configuration data.
        meta: Metadata reference.
        service: Service details.
        audit: Audit information (created, updated events).
    """

    name: str | None
    icon: str | None
    revision: int | None
    status: str | None
    website: str | None
    short_description: str | None
    long_description: str | None
    vendor: BaseModel | None
    categories: list[BaseModel] | None
    modules: list[BaseModel] | None
    statistics: BaseModel | None
    configuration: BaseModel | None
    meta: BaseModel | None
    service: BaseModel | None
    audit: BaseModel | None


class ExtensionsServiceConfig:
    """Extensions service configuration."""

    _endpoint = "/public/v1/integration/extensions"
    _model_class = Extension
    _collection_key = "data"
    _upload_file_key = "icon"
    _upload_data_key = "extension"


class ExtensionsService(
    ExtensionMixin[Extension],
    CreateFileMixin[Extension],
    UpdateFileMixin[Extension],
    GetMixin[Extension],
    DeleteMixin,
    CollectionMixin[Extension],
    Service[Extension],
    ExtensionsServiceConfig,
):
    """Sync service for the /public/v1/integration/extensions endpoint."""

    def terms(self, extension_id: str) -> ExtensionTermsService:
        """Return extension terms service."""
        return ExtensionTermsService(
            http_client=self.http_client, endpoint_params={"extension_id": extension_id}
        )

    def media(self, extension_id: str) -> ExtensionMediaService:
        """Return the media service for the given extension.

        Args:
            extension_id: Extension ID.

        Returns:
            ExtensionMediaService instance.
        """
        return ExtensionMediaService(
            http_client=self.http_client, endpoint_params={"extension_id": extension_id}
        )


class AsyncExtensionsService(
    AsyncExtensionMixin[Extension],
    AsyncCreateFileMixin[Extension],
    AsyncUpdateFileMixin[Extension],
    AsyncGetMixin[Extension],
    AsyncDeleteMixin,
    AsyncCollectionMixin[Extension],
    AsyncService[Extension],
    ExtensionsServiceConfig,
):
    """Async service for the /public/v1/integration/extensions endpoint."""

    def terms(self, extension_id: str) -> AsyncExtensionTermsService:
        """Return async extension terms service."""
        return AsyncExtensionTermsService(
            http_client=self.http_client, endpoint_params={"extension_id": extension_id}
        )

    def media(self, extension_id: str) -> AsyncExtensionMediaService:
        """Return the async media service for the given extension.

        Args:
            extension_id: Extension ID.

        Returns:
            AsyncExtensionMediaService instance.
        """
        return AsyncExtensionMediaService(
            http_client=self.http_client, endpoint_params={"extension_id": extension_id}
        )

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.integration.extension_term_variants import (
    AsyncExtensionTermVariantsService,
    ExtensionTermVariantsService,
)
from mpt_api_client.resources.mixins import (
    AsyncPublishableMixin,
    PublishableMixin,
)


class ExtensionTerm(Model):
    """Extension Term resource.

    Attributes:
        name: Term name.
        revision: Revision number.
        description: Term description.
        display_order: Display order of the term.
        status: Term status (Draft, Published, Unpublished, Deleted).
        extension: Reference to the parent extension.
        audit: Audit information (created, updated, published, unpublished events).
    """

    name: str | None
    revision: int | None
    description: str | None
    display_order: int | None
    status: str | None
    extension: BaseModel | None
    audit: BaseModel | None


class ExtensionTermsServiceConfig:
    """Extension Terms service configuration."""

    _endpoint = "/public/v1/integration/extensions/{extension_id}/terms"
    _model_class = ExtensionTerm
    _collection_key = "data"


class ExtensionTermsService(
    PublishableMixin[ExtensionTerm],
    ManagedResourceMixin[ExtensionTerm],
    CollectionMixin[ExtensionTerm],
    Service[ExtensionTerm],
    ExtensionTermsServiceConfig,
):
    """Sync service for the /public/v1/integration/extensions/{extensionId}/terms endpoint."""

    def variants(self, term_id: str) -> ExtensionTermVariantsService:
        """Access extension term variants service."""
        return ExtensionTermVariantsService(
            http_client=self.http_client,
            endpoint_params={
                "extension_id": self.endpoint_params["extension_id"],
                "term_id": term_id,
            },
        )


class AsyncExtensionTermsService(
    AsyncPublishableMixin[ExtensionTerm],
    AsyncManagedResourceMixin[ExtensionTerm],
    AsyncCollectionMixin[ExtensionTerm],
    AsyncService[ExtensionTerm],
    ExtensionTermsServiceConfig,
):
    """Async service for the /public/v1/integration/extensions/{extensionId}/terms endpoint."""

    def variants(self, term_id: str) -> AsyncExtensionTermVariantsService:
        """Access async extension term variants service."""
        return AsyncExtensionTermVariantsService(
            http_client=self.http_client,
            endpoint_params={
                "extension_id": self.endpoint_params["extension_id"],
                "term_id": term_id,
            },
        )

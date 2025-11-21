from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.catalog.mixins import AsyncPublishableMixin, PublishableMixin
from mpt_api_client.resources.catalog.product_term_variants import (
    AsyncTermVariantService,
    TermVariantService,
)


class Term(Model):
    """Term resource."""


class TermServiceConfig:
    """Term service configuration."""

    _endpoint = "/public/v1/catalog/products/{product_id}/terms"
    _model_class = Term
    _collection_key = "data"


class TermService(
    PublishableMixin[Term],
    ManagedResourceMixin[Term],
    CollectionMixin[Term],
    Service[Term],
    TermServiceConfig,
):
    """Term service."""

    def variants(self, term_id: str) -> TermVariantService:
        """Access term variants service."""
        return TermVariantService(
            http_client=self.http_client,
            endpoint_params={"product_id": self.endpoint_params["product_id"], "term_id": term_id},
        )


class AsyncTermService(
    AsyncPublishableMixin[Term],
    AsyncManagedResourceMixin[Term],
    AsyncCollectionMixin[Term],
    AsyncService[Term],
    TermServiceConfig,
):
    """Async Term service."""

    def variants(self, term_id: str) -> AsyncTermVariantService:
        """Access async term variants service."""
        return AsyncTermVariantService(
            http_client=self.http_client,
            endpoint_params={"product_id": self.endpoint_params["product_id"], "term_id": term_id},
        )

from mpt_api_client.http import AsyncService, CreateMixin, Service
from mpt_api_client.http.mixins import (
    AsyncCreateMixin,
    AsyncDeleteMixin,
    AsyncUpdateMixin,
    DeleteMixin,
    UpdateMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.catalog.mixins import (
    AsyncPublishableMixin,
    PublishableMixin,
)
from mpt_api_client.resources.catalog.products_documents import (
    AsyncDocumentService,
    DocumentService,
)
from mpt_api_client.resources.catalog.products_item_groups import (
    AsyncItemGroupsService,
    ItemGroupsService,
)
from mpt_api_client.resources.catalog.products_media import (
    AsyncMediaService,
    MediaService,
)
from mpt_api_client.resources.catalog.products_parameter_groups import (
    AsyncParameterGroupsService,
    ParameterGroupsService,
)
from mpt_api_client.resources.catalog.products_parameters import (
    AsyncParametersService,
    ParametersService,
)
from mpt_api_client.resources.catalog.products_templates import (
    AsyncTemplatesService,
    TemplatesService,
)


class Product(Model):
    """Product resource."""


class ProductsServiceConfig:
    """Products service configuration."""

    _endpoint = "/public/v1/catalog/products"
    _model_class = Product
    _collection_key = "data"


class ProductsService(
    CreateMixin[Product],
    DeleteMixin,
    UpdateMixin[Product],
    PublishableMixin[Product],
    Service[Product],
    ProductsServiceConfig,
):
    """Products service."""

    def item_groups(self, product_id: str) -> ItemGroupsService:
        """Return item_groups service."""
        return ItemGroupsService(
            http_client=self.http_client, endpoint_params={"product_id": product_id}
        )

    def parameter_groups(self, product_id: str) -> ParameterGroupsService:
        """Return parameter_groups service."""
        return ParameterGroupsService(
            http_client=self.http_client, endpoint_params={"product_id": product_id}
        )

    def media(self, product_id: str) -> MediaService:
        """Return media service."""
        return MediaService(
            http_client=self.http_client, endpoint_params={"product_id": product_id}
        )

    def documents(self, product_id: str) -> DocumentService:
        """Return documents service."""
        return DocumentService(
            http_client=self.http_client, endpoint_params={"product_id": product_id}
        )

    def product_parameters(self, product_id: str) -> ParametersService:
        """Return product_parameters service."""
        return ParametersService(
            http_client=self.http_client, endpoint_params={"product_id": product_id}
        )

    def templates(self, product_id: str) -> TemplatesService:
        """Return templates service."""
        return TemplatesService(
            http_client=self.http_client, endpoint_params={"product_id": product_id}
        )


class AsyncProductsService(
    AsyncCreateMixin[Product],
    AsyncDeleteMixin,
    AsyncUpdateMixin[Product],
    AsyncPublishableMixin[Product],
    AsyncService[Product],
    ProductsServiceConfig,
):
    """Products service."""

    def item_groups(self, product_id: str) -> AsyncItemGroupsService:
        """Return item_groups service."""
        return AsyncItemGroupsService(
            http_client=self.http_client, endpoint_params={"product_id": product_id}
        )

    def parameter_groups(self, product_id: str) -> AsyncParameterGroupsService:
        """Return parameter_groups service."""
        return AsyncParameterGroupsService(
            http_client=self.http_client, endpoint_params={"product_id": product_id}
        )

    def media(self, product_id: str) -> AsyncMediaService:
        """Return media service."""
        return AsyncMediaService(
            http_client=self.http_client, endpoint_params={"product_id": product_id}
        )

    def documents(self, product_id: str) -> AsyncDocumentService:
        """Return documents service."""
        return AsyncDocumentService(
            http_client=self.http_client, endpoint_params={"product_id": product_id}
        )

    def product_parameters(self, product_id: str) -> AsyncParametersService:
        """Return product_parameters service."""
        return AsyncParametersService(
            http_client=self.http_client, endpoint_params={"product_id": product_id}
        )

    def templates(self, product_id: str) -> AsyncTemplatesService:
        """Return templates service."""
        return AsyncTemplatesService(
            http_client=self.http_client, endpoint_params={"product_id": product_id}
        )

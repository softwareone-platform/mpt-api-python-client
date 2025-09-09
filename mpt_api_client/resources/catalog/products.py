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


class AsyncProductsService(
    AsyncCreateMixin[Product],
    AsyncDeleteMixin,
    AsyncUpdateMixin[Product],
    AsyncPublishableMixin[Product],
    AsyncService[Product],
    ProductsServiceConfig,
):
    """Products service."""

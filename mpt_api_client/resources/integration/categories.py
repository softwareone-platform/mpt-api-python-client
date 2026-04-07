from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateMixin,
    AsyncModifiableResourceMixin,
    CollectionMixin,
    CreateMixin,
    ModifiableResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel


class Category(Model):
    """Category resource.

    Attributes:
        name: Category name.
        revision: Revision number.
        description: Category description.
        status: Category status (Active or Disabled).
        audit: Audit information (created, updated events).
    """

    name: str | None
    revision: int | None
    description: str | None
    status: str | None
    audit: BaseModel | None


class CategoriesServiceConfig:
    """Categories service configuration."""

    _endpoint = "/public/v1/integration/categories"
    _model_class = Category
    _collection_key = "data"


class CategoriesService(
    CreateMixin[Category],
    ModifiableResourceMixin[Category],
    CollectionMixin[Category],
    Service[Category],
    CategoriesServiceConfig,
):
    """Sync service for the /public/v1/integration/categories endpoint."""


class AsyncCategoriesService(
    AsyncCreateMixin[Category],
    AsyncModifiableResourceMixin[Category],
    AsyncCollectionMixin[Category],
    AsyncService[Category],
    CategoriesServiceConfig,
):
    """Async service for the /public/v1/integration/categories endpoint."""

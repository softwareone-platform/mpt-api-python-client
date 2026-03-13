from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel


class Template(Model):
    """Template resource.

    Attributes:
        name: Template name.
        content: Template content.
        type: Template type.
        default: Whether this is the default template.
        product: Reference to the product.
        audit: Audit information (created, updated events).
    """

    name: str | None
    content: str | None
    type: str | None
    default: bool | None
    product: BaseModel | None
    audit: BaseModel | None


class TemplatesServiceConfig:
    """Templates service configuration."""

    _endpoint = "/public/v1/catalog/products/{product_id}/templates"
    _model_class = Template
    _collection_key = "data"


class TemplatesService(
    ManagedResourceMixin[Template],
    CollectionMixin[Template],
    Service[Template],
    TemplatesServiceConfig,
):
    """Templates service."""


class AsyncTemplatesService(
    AsyncManagedResourceMixin[Template],
    AsyncCollectionMixin[Template],
    AsyncService[Template],
    TemplatesServiceConfig,
):
    """Templates service."""

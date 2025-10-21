from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model


class Template(Model):
    """Template resource."""


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

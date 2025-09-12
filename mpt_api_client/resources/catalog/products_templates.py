from mpt_api_client.http import AsyncService, CreateMixin, DeleteMixin, Service
from mpt_api_client.http.mixins import (
    AsyncCreateMixin,
    AsyncDeleteMixin,
    AsyncUpdateMixin,
    UpdateMixin,
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
    CreateMixin[Template],
    DeleteMixin,
    UpdateMixin[Template],
    Service[Template],
    TemplatesServiceConfig,
):
    """Templates service."""


class AsyncTemplatesService(
    AsyncCreateMixin[Template],
    AsyncDeleteMixin,
    AsyncUpdateMixin[Template],
    AsyncService[Template],
    TemplatesServiceConfig,
):
    """Templates service."""

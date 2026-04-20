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
        default: Whether this is the default template.
        external_ids: External identifiers.
        type: Template type.
        status: Template status.
        program: Reference to the program.
        audit: Audit information (created, updated events).
    """

    name: str | None
    content: str | None  # noqa: WPS110
    default: bool | None
    external_ids: BaseModel | None
    type: str | None
    status: str | None
    program: BaseModel | None
    audit: BaseModel | None


class TemplatesServiceConfig:
    """Templates service configuration."""

    _endpoint = "/public/v1/program/programs/{program_id}/templates"
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

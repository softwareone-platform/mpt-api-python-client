from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel


class Footer(Model):
    """Notifications Footer resource.

    Attributes:
        language_code: Language code of the footer.
        content: Content of the footer.
        is_default: Whether this footer is the default one.
        status: Footer status.
        audit: Audit information (created, updated events).
    """

    language_code: str | None
    content: str | None
    is_default: bool | None
    status: str | None
    audit: BaseModel | None


class FootersServiceConfig:
    """Notifications Footers service configuration."""

    _endpoint = "/public/v1/notifications/footers"
    _model_class = Footer
    _collection_key = "data"


class FootersService(
    ManagedResourceMixin[Footer],
    CollectionMixin[Footer],
    Service[Footer],
    FootersServiceConfig,
):
    """Notifications Footers service."""


class AsyncFootersService(
    AsyncManagedResourceMixin[Footer],
    AsyncCollectionMixin[Footer],
    AsyncService[Footer],
    FootersServiceConfig,
):
    """Async Notifications Footers service."""

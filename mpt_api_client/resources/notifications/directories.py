from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncGetMixin,
    CollectionMixin,
    GetMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel


class Directory(Model):
    """Notifications Directory resource.

    Attributes:
        account: Reference to the account owning the directory.
        origin: Reference to the account the directory originates from.
        type: Directory type.
        contacts: References to the contacts belonging to the directory.
        audit: Audit information (created, updated events).
    """

    account: BaseModel | None
    origin: BaseModel | None
    type: str | None
    contacts: list[BaseModel] | None
    audit: BaseModel | None


class DirectoriesServiceConfig:
    """Notifications Directories service configuration."""

    _endpoint = "/public/v1/notifications/directories"
    _model_class = Directory
    _collection_key = "data"


class DirectoriesService(
    GetMixin[Directory],
    CollectionMixin[Directory],
    Service[Directory],
    DirectoriesServiceConfig,
):
    """Notifications Directories service."""


class AsyncDirectoriesService(
    AsyncGetMixin[Directory],
    AsyncCollectionMixin[Directory],
    AsyncService[Directory],
    DirectoriesServiceConfig,
):
    """Async Notifications Directories service."""

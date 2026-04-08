from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateMixin,
    AsyncGetMixin,
    CollectionMixin,
    CreateMixin,
    GetMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel


class ExtensionInstance(Model):
    """Extension Instance resource.

    Attributes:
        name: Instance name.
        revision: Revision number.
        extension: Reference to the extension.
        meta: Extension metadata reference.
        external_id: External identifier for the instance.
        status: Instance status (Connecting, Disconnected, Running, Deleted).
        channel: Channel configuration.
        audit: Audit information (created, updated, connecting, running, disconnected).
    """

    name: str | None
    revision: int | None
    extension: BaseModel | None
    meta: BaseModel | None
    external_id: str | None
    status: str | None
    channel: BaseModel | None
    audit: BaseModel | None


class ExtensionInstancesServiceConfig:
    """Extension Instances service configuration."""

    _endpoint = "/public/v1/integration/extensions/{extension_id}/instances"
    _model_class = ExtensionInstance
    _collection_key = "data"


class ExtensionInstancesService(
    CreateMixin[ExtensionInstance],
    GetMixin[ExtensionInstance],
    CollectionMixin[ExtensionInstance],
    Service[ExtensionInstance],
    ExtensionInstancesServiceConfig,
):
    """Sync service for /public/v1/integration/extensions/{extensionId}/instances endpoint."""


class AsyncExtensionInstancesService(
    AsyncCreateMixin[ExtensionInstance],
    AsyncGetMixin[ExtensionInstance],
    AsyncCollectionMixin[ExtensionInstance],
    AsyncService[ExtensionInstance],
    ExtensionInstancesServiceConfig,
):
    """Async service for /public/v1/integration/extensions/{extensionId}/instances endpoint."""

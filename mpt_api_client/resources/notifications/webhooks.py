from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncDisableMixin,
    AsyncEnableMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    DisableMixin,
    EnableMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel


class Webhook(Model):
    """Notifications Webhook resource.

    Attributes:
        name: Webhook name.
        url: Endpoint the webhook calls.
        description: Webhook description.
        status: Webhook status.
        type: Webhook type.
        secret: Shared secret used to sign webhook calls.
        statistics: Call statistics of the webhook.
        object_type: Type of the object the webhook is bound to.
        account: Reference to the account owning the webhook.
        object: Reference to the object the webhook is bound to.
        criteria: Key/value criteria narrowing when the webhook fires.
        last_success: Last successful call.
        last_failure: Last failed call.
        last_call: Last call regardless of its outcome.
        audit: Audit information (created, updated events).
    """

    name: str | None
    url: str | None
    description: str | None
    status: str | None
    type: str | None
    secret: str | None
    statistics: BaseModel | None
    object_type: str | None
    account: BaseModel | None
    object: BaseModel | None
    criteria: list[BaseModel] | None
    last_success: BaseModel | None
    last_failure: BaseModel | None
    last_call: BaseModel | None
    audit: BaseModel | None


class WebhooksServiceConfig:
    """Notifications Webhooks service configuration."""

    _endpoint = "/public/v1/notifications/webhooks"
    _model_class = Webhook
    _collection_key = "data"


class WebhooksService(
    EnableMixin[Webhook],
    DisableMixin[Webhook],
    ManagedResourceMixin[Webhook],
    CollectionMixin[Webhook],
    Service[Webhook],
    WebhooksServiceConfig,
):
    """Notifications Webhooks service."""


class AsyncWebhooksService(
    AsyncEnableMixin[Webhook],
    AsyncDisableMixin[Webhook],
    AsyncManagedResourceMixin[Webhook],
    AsyncCollectionMixin[Webhook],
    AsyncService[Webhook],
    WebhooksServiceConfig,
):
    """Async Notifications Webhooks service."""

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.models import Model


class Message(Model):
    """Notifications Message resource."""


class MessagesServiceConfig:
    """Notifications Messages service configuration."""

    _endpoint = "/public/v1/notifications/messages"
    _model_class = Message
    _collection_key = "data"


class MessagesService(
    Service[Message],
    MessagesServiceConfig,
):
    """Notifications Messages service (no CRUD, no block/unblock)."""


class AsyncMessagesService(
    AsyncService[Message],
    MessagesServiceConfig,
):
    """Async Notifications Messages service (no CRUD, no block/unblock)."""

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncGetMixin,
    CollectionMixin,
    GetMixin,
)
from mpt_api_client.models import Model


class Message(Model):
    """Notifications Message resource."""


class MessagesServiceConfig:
    """Notifications Messages service configuration."""

    _endpoint = "/public/v1/notifications/messages"
    _model_class = Message
    _collection_key = "data"


class MessagesService(
    GetMixin[Message],
    CollectionMixin[Message],
    Service[Message],
    MessagesServiceConfig,
):
    """Notifications Messages service."""


class AsyncMessagesService(
    AsyncGetMixin[Message],
    AsyncCollectionMixin[Message],
    AsyncService[Message],
    MessagesServiceConfig,
):
    """Async Notifications Messages service."""

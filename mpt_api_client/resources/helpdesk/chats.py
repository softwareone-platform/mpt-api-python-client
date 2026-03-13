from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateMixin,
    AsyncGetMixin,
    AsyncUpdateMixin,
    CollectionMixin,
    CreateMixin,
    GetMixin,
    UpdateMixin,
)
from mpt_api_client.models import Model


class Chat(Model):
    """Helpdesk Chat resource."""


class ChatsServiceConfig:
    """Helpdesk Chats service configuration."""

    _endpoint = "/public/v1/helpdesk/chats"
    _model_class = Chat
    _collection_key = "data"


class ChatsService(
    CreateMixin[Chat],
    UpdateMixin[Chat],
    GetMixin[Chat],
    CollectionMixin[Chat],
    Service[Chat],
    ChatsServiceConfig,
):
    """Helpdesk Chats service."""


class AsyncChatsService(
    AsyncCreateMixin[Chat],
    AsyncUpdateMixin[Chat],
    AsyncGetMixin[Chat],
    AsyncCollectionMixin[Chat],
    AsyncService[Chat],
    ChatsServiceConfig,
):
    """Async Helpdesk Chats service."""

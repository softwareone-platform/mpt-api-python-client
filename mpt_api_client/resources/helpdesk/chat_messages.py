from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateMixin,
    AsyncDeleteMixin,
    AsyncUpdateMixin,
    CollectionMixin,
    CreateMixin,
    DeleteMixin,
    UpdateMixin,
)
from mpt_api_client.models import Model


class ChatMessage(Model):
    """Helpdesk Chat Message resource."""


class ChatMessagesServiceConfig:
    """Helpdesk Chat Messages service configuration."""

    _endpoint = "/public/v1/helpdesk/chats/{chat_id}/messages"
    _model_class = ChatMessage
    _collection_key = "data"


class ChatMessagesService(
    CreateMixin[ChatMessage],
    UpdateMixin[ChatMessage],
    DeleteMixin,
    CollectionMixin[ChatMessage],
    Service[ChatMessage],
    ChatMessagesServiceConfig,
):
    """Helpdesk Chat Messages service."""


class AsyncChatMessagesService(
    AsyncCreateMixin[ChatMessage],
    AsyncUpdateMixin[ChatMessage],
    AsyncDeleteMixin,
    AsyncCollectionMixin[ChatMessage],
    AsyncService[ChatMessage],
    ChatMessagesServiceConfig,
):
    """Async Helpdesk Chat Messages service."""

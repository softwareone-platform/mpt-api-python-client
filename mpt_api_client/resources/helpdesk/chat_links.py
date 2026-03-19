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


class ChatLink(Model):
    """Helpdesk Chat Link resource."""


class ChatLinksServiceConfig:
    """Helpdesk Chat Links service configuration."""

    _endpoint = "/public/v1/helpdesk/chats/{chat_id}/links"
    _model_class = ChatLink
    _collection_key = "data"


class ChatLinksService(
    CreateMixin[ChatLink],
    UpdateMixin[ChatLink],
    DeleteMixin,
    CollectionMixin[ChatLink],
    Service[ChatLink],
    ChatLinksServiceConfig,
):
    """Helpdesk Chat Links service."""


class AsyncChatLinksService(
    AsyncCreateMixin[ChatLink],
    AsyncUpdateMixin[ChatLink],
    AsyncDeleteMixin,
    AsyncCollectionMixin[ChatLink],
    AsyncService[ChatLink],
    ChatLinksServiceConfig,
):
    """Async Helpdesk Chat Links service."""

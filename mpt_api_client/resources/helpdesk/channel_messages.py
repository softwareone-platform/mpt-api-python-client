from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import AsyncCollectionMixin, CollectionMixin
from mpt_api_client.resources.helpdesk.chat_messages import ChatMessage


class ChannelMessagesServiceConfig:
    """Helpdesk channel messages service configuration."""

    _endpoint = "/public/v1/helpdesk/channels/{channel_id}/messages"
    _model_class = ChatMessage
    _collection_key = "data"


class ChannelMessagesService(
    CollectionMixin[ChatMessage],
    Service[ChatMessage],
    ChannelMessagesServiceConfig,
):
    """Helpdesk channel messages service."""


class AsyncChannelMessagesService(
    AsyncCollectionMixin[ChatMessage],
    AsyncService[ChatMessage],
    ChannelMessagesServiceConfig,
):
    """Async helpdesk channel messages service."""

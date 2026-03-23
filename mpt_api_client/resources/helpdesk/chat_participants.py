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


class ChatParticipant(Model):
    """Helpdesk Chat Participant resource."""


class ChatParticipantsServiceConfig:
    """Helpdesk Chat Participants service configuration."""

    _endpoint = "/public/v1/helpdesk/chats/{chat_id}/participants"
    _model_class = ChatParticipant
    _collection_key = "data"


class ChatParticipantsService(
    CreateMixin[ChatParticipant],
    UpdateMixin[ChatParticipant],
    DeleteMixin,
    CollectionMixin[ChatParticipant],
    Service[ChatParticipant],
    ChatParticipantsServiceConfig,
):
    """Helpdesk Chat Participants service."""


class AsyncChatParticipantsService(
    AsyncCreateMixin[ChatParticipant],
    AsyncUpdateMixin[ChatParticipant],
    AsyncDeleteMixin,
    AsyncCollectionMixin[ChatParticipant],
    AsyncService[ChatParticipant],
    ChatParticipantsServiceConfig,
):
    """Async Helpdesk Chat Participants service."""

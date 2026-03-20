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
from mpt_api_client.resources.helpdesk.chat_attachments import (
    AsyncChatAttachmentsService,
    ChatAttachmentsService,
)
from mpt_api_client.resources.helpdesk.chat_links import (
    AsyncChatLinksService,
    ChatLinksService,
)
from mpt_api_client.resources.helpdesk.chat_messages import (
    AsyncChatMessagesService,
    ChatMessagesService,
)
from mpt_api_client.resources.helpdesk.chat_participants import (
    AsyncChatParticipantsService,
    ChatParticipantsService,
)


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

    def attachments(self, chat_id: str) -> ChatAttachmentsService:
        """Return chat attachments service."""
        return ChatAttachmentsService(
            http_client=self.http_client, endpoint_params={"chat_id": chat_id}
        )

    def messages(self, chat_id: str) -> ChatMessagesService:
        """Return chat messages service."""
        return ChatMessagesService(
            http_client=self.http_client, endpoint_params={"chat_id": chat_id}
        )

    def links(self, chat_id: str) -> ChatLinksService:
        """Return chat links service."""
        return ChatLinksService(http_client=self.http_client, endpoint_params={"chat_id": chat_id})

    def participants(self, chat_id: str) -> ChatParticipantsService:
        """Return chat participants service."""
        return ChatParticipantsService(
            http_client=self.http_client, endpoint_params={"chat_id": chat_id}
        )


class AsyncChatsService(
    AsyncCreateMixin[Chat],
    AsyncUpdateMixin[Chat],
    AsyncGetMixin[Chat],
    AsyncCollectionMixin[Chat],
    AsyncService[Chat],
    ChatsServiceConfig,
):
    """Async Helpdesk Chats service."""

    def attachments(self, chat_id: str) -> AsyncChatAttachmentsService:
        """Return async chat attachments service."""
        return AsyncChatAttachmentsService(
            http_client=self.http_client, endpoint_params={"chat_id": chat_id}
        )

    def messages(self, chat_id: str) -> AsyncChatMessagesService:
        """Return async chat messages service."""
        return AsyncChatMessagesService(
            http_client=self.http_client, endpoint_params={"chat_id": chat_id}
        )

    def links(self, chat_id: str) -> AsyncChatLinksService:
        """Return async chat links service."""
        return AsyncChatLinksService(
            http_client=self.http_client, endpoint_params={"chat_id": chat_id}
        )

    def participants(self, chat_id: str) -> AsyncChatParticipantsService:
        """Return async chat participants service."""
        return AsyncChatParticipantsService(
            http_client=self.http_client, endpoint_params={"chat_id": chat_id}
        )

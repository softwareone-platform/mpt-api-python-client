from mpt_api_client.http import AsyncService, Service, mixins
from mpt_api_client.models import Model, ResourceData
from mpt_api_client.resources.helpdesk.chat_answer_parameters import (
    AsyncChatAnswerParametersService,
    ChatAnswerParametersService,
)


class ChatAnswer(Model):
    """Helpdesk Chat Answer resource."""


class ChatAnswersServiceConfig:
    """Helpdesk Chat Answers service configuration."""

    _endpoint = "/public/v1/helpdesk/chats/{chat_id}/answers"
    _model_class = ChatAnswer
    _collection_key = "data"


class ChatAnswersService(
    mixins.CreateMixin[ChatAnswer],
    mixins.UpdateMixin[ChatAnswer],
    mixins.DeleteMixin,
    mixins.GetMixin[ChatAnswer],
    mixins.CollectionMixin[ChatAnswer],
    Service[ChatAnswer],
    ChatAnswersServiceConfig,
):
    """Helpdesk Chat Answers service."""

    def submit(self, resource_id: str, resource_data: ResourceData | None = None) -> ChatAnswer:
        """Switch answer to submitted state."""
        return self._resource_action(resource_id, "POST", "submit", json=resource_data)

    def accept(self, resource_id: str, resource_data: ResourceData | None = None) -> ChatAnswer:
        """Switch answer to accepted state."""
        return self._resource_action(resource_id, "POST", "accept", json=resource_data)

    def query(self, resource_id: str, resource_data: ResourceData | None = None) -> ChatAnswer:
        """Switch answer to query state."""
        return self._resource_action(resource_id, "POST", "query", json=resource_data)

    def validate(self, resource_id: str, resource_data: ResourceData | None = None) -> ChatAnswer:
        """Validate answer."""
        return self._resource_action(resource_id, "POST", "validate", json=resource_data)

    def parameters(self, answer_id: str) -> ChatAnswerParametersService:  # noqa: WPS110
        """Return chat answer parameters service."""
        return ChatAnswerParametersService(
            http_client=self.http_client,
            endpoint_params={
                "chat_id": self.endpoint_params["chat_id"],
                "answer_id": answer_id,
            },
        )


class AsyncChatAnswersService(
    mixins.AsyncCreateMixin[ChatAnswer],
    mixins.AsyncUpdateMixin[ChatAnswer],
    mixins.AsyncDeleteMixin,
    mixins.AsyncGetMixin[ChatAnswer],
    mixins.AsyncCollectionMixin[ChatAnswer],
    AsyncService[ChatAnswer],
    ChatAnswersServiceConfig,
):
    """Async Helpdesk Chat Answers service."""

    async def submit(
        self,
        resource_id: str,
        resource_data: ResourceData | None = None,
    ) -> ChatAnswer:
        """Switch answer to submitted state."""
        return await self._resource_action(resource_id, "POST", "submit", json=resource_data)

    async def accept(
        self,
        resource_id: str,
        resource_data: ResourceData | None = None,
    ) -> ChatAnswer:
        """Switch answer to accepted state."""
        return await self._resource_action(resource_id, "POST", "accept", json=resource_data)

    async def query(
        self,
        resource_id: str,
        resource_data: ResourceData | None = None,
    ) -> ChatAnswer:
        """Switch answer to query state."""
        return await self._resource_action(resource_id, "POST", "query", json=resource_data)

    async def validate(
        self,
        resource_id: str,
        resource_data: ResourceData | None = None,
    ) -> ChatAnswer:
        """Validate answer."""
        return await self._resource_action(resource_id, "POST", "validate", json=resource_data)

    def parameters(self, answer_id: str) -> AsyncChatAnswerParametersService:  # noqa: WPS110
        """Return async chat answer parameters service."""
        return AsyncChatAnswerParametersService(
            http_client=self.http_client,
            endpoint_params={
                "chat_id": self.endpoint_params["chat_id"],
                "answer_id": answer_id,
            },
        )

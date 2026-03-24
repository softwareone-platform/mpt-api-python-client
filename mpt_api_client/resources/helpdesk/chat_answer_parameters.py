from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import AsyncCollectionMixin, CollectionMixin
from mpt_api_client.models import Model


class ChatAnswerParameter(Model):
    """Helpdesk chat answer parameter resource."""


class ChatAnswerParametersServiceConfig:
    """Helpdesk chat answer parameters service configuration."""

    _endpoint = "/public/v1/helpdesk/chats/{chat_id}/answers/{answer_id}/parameters"
    _model_class = ChatAnswerParameter
    _collection_key = "data"


class ChatAnswerParametersService(
    CollectionMixin[ChatAnswerParameter],
    Service[ChatAnswerParameter],
    ChatAnswerParametersServiceConfig,
):
    """Helpdesk chat answer parameters service."""


class AsyncChatAnswerParametersService(
    AsyncCollectionMixin[ChatAnswerParameter],
    AsyncService[ChatAnswerParameter],
    ChatAnswerParametersServiceConfig,
):
    """Async helpdesk chat answer parameters service."""

from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources.helpdesk.cases import AsyncCasesService, CasesService
from mpt_api_client.resources.helpdesk.chats import AsyncChatsService, ChatsService
from mpt_api_client.resources.helpdesk.parameters import (
    AsyncParametersService,
    ParametersService,
)
from mpt_api_client.resources.helpdesk.queues import AsyncQueuesService, QueuesService


class Helpdesk:
    """Helpdesk MPT API Module."""

    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client

    @property
    def chats(self) -> ChatsService:
        """Chats service."""
        return ChatsService(http_client=self.http_client)

    @property
    def cases(self) -> CasesService:
        """Cases service."""
        return CasesService(http_client=self.http_client)

    @property
    def queues(self) -> QueuesService:
        """Queues service."""
        return QueuesService(http_client=self.http_client)

    @property
    def parameters(self) -> ParametersService:  # noqa: WPS110
        """Parameters service."""
        return ParametersService(http_client=self.http_client)


class AsyncHelpdesk:
    """Async Helpdesk MPT API Module."""

    def __init__(self, http_client: AsyncHTTPClient):
        self.http_client = http_client

    @property
    def chats(self) -> AsyncChatsService:
        """Async Chats service."""
        return AsyncChatsService(http_client=self.http_client)

    @property
    def cases(self) -> AsyncCasesService:
        """Async Cases service."""
        return AsyncCasesService(http_client=self.http_client)

    @property
    def queues(self) -> AsyncQueuesService:
        """Async Queues service."""
        return AsyncQueuesService(http_client=self.http_client)

    @property
    def parameters(self) -> AsyncParametersService:  # noqa: WPS110
        """Async parameters service."""
        return AsyncParametersService(http_client=self.http_client)

from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources.helpdesk.cases import AsyncCasesService, CasesService
from mpt_api_client.resources.helpdesk.chats import AsyncChatsService, ChatsService


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

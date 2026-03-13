from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources.helpdesk.chats import AsyncChatsService, ChatsService


class Helpdesk:
    """Helpdesk MPT API Module."""

    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client

    @property
    def chats(self) -> ChatsService:
        """Chats service."""
        return ChatsService(http_client=self.http_client)


class AsyncHelpdesk:
    """Async Helpdesk MPT API Module."""

    def __init__(self, http_client: AsyncHTTPClient):
        self.http_client = http_client

    @property
    def chats(self) -> AsyncChatsService:
        """Async Chats service."""
        return AsyncChatsService(http_client=self.http_client)

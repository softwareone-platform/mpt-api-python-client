from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources.notifications.categories import (
    AsyncCategoriesService,
    CategoriesService,
)
from mpt_api_client.resources.notifications.contacts import AsyncContactsService, ContactsService


class Notifications:
    """Notifications MPT API Module."""

    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client

    @property
    def categories(self) -> CategoriesService:
        """Categories service."""
        return CategoriesService(http_client=self.http_client)

    @property
    def contacts(self) -> ContactsService:
        """Contacts service."""
        return ContactsService(http_client=self.http_client)


class AsyncNotifications:
    """Notifications MPT API Module."""

    def __init__(self, http_client: AsyncHTTPClient):
        self.http_client = http_client

    @property
    def categories(self) -> AsyncCategoriesService:
        """Categories service."""
        return AsyncCategoriesService(http_client=self.http_client)

    @property
    def contacts(self) -> AsyncContactsService:
        """Async Contacts service."""
        return AsyncContactsService(http_client=self.http_client)

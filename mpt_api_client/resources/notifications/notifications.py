from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources.notifications.accounts import AccountsService, AsyncAccountsService
from mpt_api_client.resources.notifications.batches import AsyncBatchesService, BatchesService
from mpt_api_client.resources.notifications.categories import (
    AsyncCategoriesService,
    CategoriesService,
)
from mpt_api_client.resources.notifications.contacts import AsyncContactsService, ContactsService
from mpt_api_client.resources.notifications.messages import AsyncMessagesService, MessagesService
from mpt_api_client.resources.notifications.subscribers import (
    AsyncSubscribersService,
    SubscribersService,
)


class Notifications:
    """Notifications MPT API Module."""

    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client

    def accounts(self, account_id: str, category_id: str) -> AccountsService:
        """Accounts service.

        Returns contacts, which are configured to receive notifications.

        Parms:
            account_id: Account ID
            category_id: Category ID

        Returns:
            AccountsService
        """
        return AccountsService(
            http_client=self.http_client,
            endpoint_params={"account_id": account_id, "category_id": category_id},
        )

    @property
    def batches(self) -> BatchesService:
        """Batches service."""
        return BatchesService(http_client=self.http_client)

    @property
    def categories(self) -> CategoriesService:
        """Categories service."""
        return CategoriesService(http_client=self.http_client)

    @property
    def contacts(self) -> ContactsService:
        """Contacts service."""
        return ContactsService(http_client=self.http_client)

    @property
    def messages(self) -> MessagesService:
        """Messages service."""
        return MessagesService(http_client=self.http_client)

    @property
    def subscribers(self) -> SubscribersService:
        """Subscriptions service."""
        return SubscribersService(http_client=self.http_client)


class AsyncNotifications:
    """Notifications MPT API Module."""

    def __init__(self, http_client: AsyncHTTPClient):
        self.http_client = http_client

    def accounts(self, account_id: str, category_id: str) -> AsyncAccountsService:
        """Async Accounts service.

        Returns contacts, which are configured to receive notifications.

        Parms:
            account_id: Account ID
            category_id: Category ID

        Returns:
            AccountsService
        """
        return AsyncAccountsService(
            http_client=self.http_client,
            endpoint_params={"account_id": account_id, "category_id": category_id},
        )

    @property
    def batches(self) -> AsyncBatchesService:
        """Batches service."""
        return AsyncBatchesService(http_client=self.http_client)

    @property
    def categories(self) -> AsyncCategoriesService:
        """Categories service."""
        return AsyncCategoriesService(http_client=self.http_client)

    @property
    def contacts(self) -> AsyncContactsService:
        """Async Contacts service."""
        return AsyncContactsService(http_client=self.http_client)

    @property
    def messages(self) -> AsyncMessagesService:
        """Async Messages service."""
        return AsyncMessagesService(http_client=self.http_client)

    @property
    def subscribers(self) -> AsyncSubscribersService:
        """Subscriptions service."""
        return AsyncSubscribersService(http_client=self.http_client)

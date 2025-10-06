import pytest

from mpt_api_client.resources import AsyncNotifications, Notifications
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


def test_notifications_init(http_client):
    commerce = Notifications(http_client=http_client)

    assert isinstance(commerce, Notifications)
    assert commerce.http_client is http_client


def test_async_notifications_init(async_http_client):
    notifications = AsyncNotifications(http_client=async_http_client)

    assert isinstance(notifications, AsyncNotifications)
    assert notifications.http_client is async_http_client


@pytest.mark.parametrize(
    ("attr_name", "expected"),
    [
        ("categories", CategoriesService),
        ("contacts", ContactsService),
        ("messages", MessagesService),
        ("batches", BatchesService),
        ("subscribers", SubscribersService),
    ],
)
def test_notifications_properties(http_client, attr_name, expected):
    notifications = Notifications(http_client=http_client)

    service = getattr(notifications, attr_name)

    assert isinstance(service, expected)


@pytest.mark.parametrize(
    ("attr_name", "expected"),
    [
        ("categories", AsyncCategoriesService),
        ("contacts", AsyncContactsService),
        ("messages", AsyncMessagesService),
        ("batches", AsyncBatchesService),
        ("subscribers", AsyncSubscribersService),
    ],
)
def test_async_notifications_properties(http_client, attr_name, expected):
    notifications = AsyncNotifications(http_client=http_client)

    service = getattr(notifications, attr_name)

    assert isinstance(service, expected)


def test_notifications_accounts(http_client):
    notifications = Notifications(http_client=http_client)
    account_id = "ACC-123"
    category_id = "CAT-456"
    service = notifications.accounts(account_id, category_id)
    assert isinstance(service, AccountsService)
    assert service.endpoint_params == {"account_id": account_id, "category_id": category_id}


def test_async_notifications_accounts(async_http_client):
    notifications = AsyncNotifications(http_client=async_http_client)
    account_id = "ACC-123"
    category_id = "CAT-456"
    service = notifications.accounts(account_id, category_id)
    assert isinstance(service, AsyncAccountsService)
    assert service.endpoint_params == {"account_id": account_id, "category_id": category_id}

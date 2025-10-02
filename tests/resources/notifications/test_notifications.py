import pytest

from mpt_api_client.resources import AsyncNotifications, Notifications
from mpt_api_client.resources.notifications.categories import (
    AsyncCategoriesService,
    CategoriesService,
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
    ],
)
def test_notifications_properties(http_client, attr_name, expected):
    commerce = Notifications(http_client=http_client)

    service = getattr(commerce, attr_name)

    assert isinstance(service, expected)


@pytest.mark.parametrize(
    ("attr_name", "expected"),
    [
        ("categories", AsyncCategoriesService),
    ],
)
def test_async_notifications_properties(http_client, attr_name, expected):
    commerce = AsyncNotifications(http_client=http_client)

    service = getattr(commerce, attr_name)

    assert isinstance(service, expected)

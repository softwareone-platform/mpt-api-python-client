from mpt_api_client.exceptions import MPTError
from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import AsyncCollectionMixin, CollectionMixin
from mpt_api_client.models import Model


class MethodNotAllowedError(MPTError):
    """Method not allowed error."""


class NotificationContact(Model):
    """Notification Contact resource."""


class AccountsServiceConfig:
    """Accounts service config."""

    _endpoint = "/public/v1/notifications/accounts/{account_id}/categories/{category_id}/contacts"
    _model_class = NotificationContact
    _collection_key = "data"


class AccountsService(
    CollectionMixin[NotificationContact], Service[NotificationContact], AccountsServiceConfig
):
    """Accounts service."""


class AsyncAccountsService(
    AsyncCollectionMixin[NotificationContact],
    AsyncService[NotificationContact],
    AccountsServiceConfig,
):
    """Async Accounts service."""

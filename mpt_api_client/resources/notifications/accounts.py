from mpt_api_client.exceptions import MPTError
from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import AsyncCollectionMixin, CollectionMixin
from mpt_api_client.models import Model


class MethodNotAllowedError(MPTError):
    """Method not allowed error."""


class Contact(Model):
    """Account resource."""


class AccountsServiceConfig:
    """Accounts service config."""

    _endpoint = "/public/v1/notifications/accounts/{account_id}/categories/{category_id}/contacts"
    _model_class = Contact
    _collection_key = "data"


class AccountsService(CollectionMixin[Contact], Service[Contact], AccountsServiceConfig):
    """Accounts service."""


class AsyncAccountsService(
    AsyncCollectionMixin[Contact], AsyncService[Contact], AccountsServiceConfig
):
    """Async Accounts service."""

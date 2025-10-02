from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCreateMixin,
    AsyncUpdateMixin,
    CreateMixin,
    UpdateMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.accounts.mixins import (
    ActivatableMixin,
    AsyncActivatableMixin,
    AsyncEnablableMixin,
    AsyncValidateMixin,
    EnablableMixin,
    ValidateMixin,
)


class Account(Model):
    """Account resource."""


class AccountsServiceConfig:
    """Accounts service configuration."""

    _endpoint = "/public/v1/accounts"
    _model_class = Account
    _collection_key = "data"


class AccountsService(
    CreateMixin[Account],
    UpdateMixin[Account],
    ActivatableMixin[Account],
    EnablableMixin[Account],
    ValidateMixin[Account],
    Service[Account],
    AccountsServiceConfig,
):
    """Accounts service."""


class AsyncAccountsService(
    AsyncCreateMixin[Account],
    AsyncUpdateMixin[Account],
    AsyncActivatableMixin[Account],
    AsyncEnablableMixin[Account],
    AsyncValidateMixin[Account],
    AsyncService[Account],
    AccountsServiceConfig,
):
    """Async Accounts service."""

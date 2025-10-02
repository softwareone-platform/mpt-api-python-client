from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCreateMixin,
    AsyncUpdateMixin,
    CreateMixin,
    UpdateMixin,
)
from mpt_api_client.models import Model


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
    Service[Account],
    AccountsServiceConfig,
):
    """Accounts service."""


class AsyncAccountsService(
    AsyncCreateMixin[Account],
    AsyncUpdateMixin[Account],
    AsyncService[Account],
    AccountsServiceConfig,
):
    """Async Accounts service."""

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCreateMixin,
    AsyncDeleteMixin,
    AsyncUpdateMixin,
    CreateMixin,
    DeleteMixin,
    UpdateMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.accounts.mixins import (
    AsyncInvitableMixin,
    InvitableMixin,
)


class AccountsUser(Model):
    """Account User Model."""


class AccountsUsersServiceConfig:
    """Account Users Service Configuration."""

    _endpoint = "/public/v1/accounts/accounts/{account_id}/users"
    _model_class = AccountsUser
    _collection_key = "data"


class AccountsUsersService(
    UpdateMixin[AccountsUser],
    DeleteMixin,
    CreateMixin[AccountsUser],
    InvitableMixin[AccountsUser],
    Service[AccountsUser],
    AccountsUsersServiceConfig,
):
    """Account Users Service."""


class AsyncAccountsUsersService(
    AsyncUpdateMixin[AccountsUser],
    AsyncDeleteMixin,
    AsyncCreateMixin[AccountsUser],
    AsyncService[AccountsUser],
    AsyncInvitableMixin[AccountsUser],
    AccountsUsersServiceConfig,
):
    """Asynchronous Account Users Service."""

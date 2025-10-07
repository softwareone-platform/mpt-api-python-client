from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCreateMixin,
    CreateMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.accounts.mixins import (
    AsyncInvitableMixin,
    InvitableMixin,
)


class AccountUser(Model):
    """Account User Model."""


class AccountUsersServiceConfig:
    """Account Users Service Configuration."""

    _endpoint = "/public/v1/accounts/account-users"
    _model_class = AccountUser
    _collection_key = "data"


class AccountUsersService(
    CreateMixin[AccountUser],
    InvitableMixin[AccountUser],
    Service[AccountUser],
    AccountUsersServiceConfig,
):
    """Account Users Service."""


class AsyncAccountUsersService(
    AsyncCreateMixin[AccountUser],
    AsyncService[AccountUser],
    AsyncInvitableMixin[AccountUser],
    AccountUsersServiceConfig,
):
    """Asynchronous Account Users Service."""

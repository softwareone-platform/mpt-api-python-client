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


class AccountsUserGroup(Model):
    """Account User Group Model."""


class AccountsUserGroupsServiceConfig:
    """Account User Groups Service Configuration."""

    _endpoint = "/public/v1/accounts/{account_id}/users/{user_id}/groups"
    _model_class = AccountsUserGroup
    _collection_key = "data"


class AccountsUserGroupsService(
    UpdateMixin[AccountsUserGroup],
    DeleteMixin,
    CreateMixin[AccountsUserGroup],
    Service[AccountsUserGroup],
    AccountsUserGroupsServiceConfig,
):
    """Account User Groups Service."""


class AsyncAccountsUserGroupsService(
    AsyncUpdateMixin[AccountsUserGroup],
    AsyncDeleteMixin,
    AsyncCreateMixin[AccountsUserGroup],
    AsyncService[AccountsUserGroup],
    AccountsUserGroupsServiceConfig,
):
    """Asynchronous Account User Groups Service."""

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCreateMixin,
    AsyncDeleteMixin,
    AsyncGetMixin,
    AsyncUpdateMixin,
    CreateMixin,
    DeleteMixin,
    GetMixin,
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
    GetMixin[AccountsUserGroup],
    CreateMixin[AccountsUserGroup],
    Service[AccountsUserGroup],
    AccountsUserGroupsServiceConfig,
):
    """Account User Groups Service."""


class AsyncAccountsUserGroupsService(
    AsyncUpdateMixin[AccountsUserGroup],
    AsyncDeleteMixin,
    AsyncGetMixin[AccountsUserGroup],
    AsyncCreateMixin[AccountsUserGroup],
    AsyncService[AccountsUserGroup],
    AccountsUserGroupsServiceConfig,
):
    """Asynchronous Account User Groups Service."""

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


class AccountUserGroup(Model):
    """Account User Group resource."""


class AccountUserGroupsServiceConfig:
    """Account User Groups service configuration."""

    _endpoint = "/public/v1/accounts/account-users/{account_user_id}/groups"
    _model_class = AccountUserGroup
    _collection_key = "data"


class AccountUserGroupsService(
    CreateMixin[AccountUserGroup],
    DeleteMixin,
    UpdateMixin[AccountUserGroup],
    Service[AccountUserGroup],
    AccountUserGroupsServiceConfig,
):
    """Account User Groups service."""


class AsyncAccountUserGroupsService(
    AsyncCreateMixin[AccountUserGroup],
    AsyncDeleteMixin,
    AsyncUpdateMixin[AccountUserGroup],
    AsyncService[AccountUserGroup],
    AccountUserGroupsServiceConfig,
):
    """Async Account User Groups service."""

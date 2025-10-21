from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
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
    ManagedResourceMixin[AccountUserGroup],
    CollectionMixin[AccountUserGroup],
    Service[AccountUserGroup],
    AccountUserGroupsServiceConfig,
):
    """Account User Groups service."""


class AsyncAccountUserGroupsService(
    AsyncManagedResourceMixin[AccountUserGroup],
    AsyncCollectionMixin[AccountUserGroup],
    AsyncService[AccountUserGroup],
    AccountUserGroupsServiceConfig,
):
    """Async Account User Groups service."""

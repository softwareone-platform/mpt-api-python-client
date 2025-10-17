from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model


class UserGroup(Model):
    """User Group resource."""


class UserGroupsServiceConfig:
    """User Groups service configuration."""

    _endpoint = "/public/v1/accounts/user-groups"
    _model_class = UserGroup
    _collection_key = "data"


class UserGroupsService(
    ManagedResourceMixin[UserGroup],
    CollectionMixin[UserGroup],
    Service[UserGroup],
    UserGroupsServiceConfig,
):
    """User Groups service."""


class AsyncUserGroupsService(
    AsyncManagedResourceMixin[UserGroup],
    AsyncCollectionMixin[UserGroup],
    AsyncService[UserGroup],
    UserGroupsServiceConfig,
):
    """Async User Groups service."""

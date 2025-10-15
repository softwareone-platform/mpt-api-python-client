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


class UserGroup(Model):
    """User Group resource."""


class UserGroupsServiceConfig:
    """User Groups service configuration."""

    _endpoint = "/public/v1/accounts/user-groups"
    _model_class = UserGroup
    _collection_key = "data"


class UserGroupsService(
    CreateMixin[UserGroup],
    UpdateMixin[UserGroup],
    DeleteMixin,
    GetMixin[UserGroup],
    Service[UserGroup],
    UserGroupsServiceConfig,
):
    """User Groups service."""


class AsyncUserGroupsService(
    AsyncCreateMixin[UserGroup],
    AsyncUpdateMixin[UserGroup],
    AsyncDeleteMixin,
    AsyncGetMixin[UserGroup],
    AsyncService[UserGroup],
    UserGroupsServiceConfig,
):
    """Async User Groups service."""

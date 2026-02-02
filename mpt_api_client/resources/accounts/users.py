from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncDeleteMixin,
    AsyncGetMixin,
    AsyncUpdateFileMixin,
    CollectionMixin,
    DeleteMixin,
    GetMixin,
    UpdateFileMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import ResourceData
from mpt_api_client.resources.accounts.mixins import (
    AsyncBlockableMixin,
    BlockableMixin,
)


class User(Model):
    """User resource."""


class UsersServiceConfig:
    """Users service configuration."""

    _endpoint = "/public/v1/accounts/users"
    _model_class = User
    _collection_key = "data"
    _upload_file_key = "icon"
    _upload_data_key = "user"


class UsersService(
    UpdateFileMixin[User],
    DeleteMixin,
    BlockableMixin[User],
    GetMixin[User],
    CollectionMixin[User],
    Service[User],
    UsersServiceConfig,
):
    """Users service."""

    def sso(self, resource_id: str, resource_data: ResourceData | None = None) -> User:
        """Perform SSO action for a user.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(resource_id, "POST", "sso", json=resource_data)

    def sso_check(self, resource_id: str, resource_data: ResourceData | None = None) -> User:
        """Perform SSO check action for a user.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(resource_id, "POST", "sso-check", json=resource_data)

    def set_password(self, resource_id: str, password: str) -> User:
        """Set password for a user.

        Args:
            resource_id: Resource ID
            password: New password
        """
        resource_data = {"password": password}

        return self._resource_action(resource_id, "POST", "set-password", json=resource_data)


class AsyncUsersService(
    AsyncUpdateFileMixin[User],
    AsyncDeleteMixin,
    AsyncBlockableMixin[User],
    AsyncGetMixin[User],
    AsyncCollectionMixin[User],
    AsyncService[User],
    UsersServiceConfig,
):
    """Async Users service."""

    async def sso(self, resource_id: str, resource_data: ResourceData | None = None) -> User:
        """Perform SSO action for a user.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(resource_id, "POST", "sso", json=resource_data)

    async def sso_check(self, resource_id: str, resource_data: ResourceData | None = None) -> User:
        """Perform SSO check action for a user.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(resource_id, "POST", "sso-check", json=resource_data)

    async def set_password(self, resource_id: str, password: str) -> User:
        """Set password for a user.

        Args:
            resource_id: Resource ID
            password: New password
        """
        resource_data = {"password": password}

        return await self._resource_action(resource_id, "POST", "set-password", json=resource_data)

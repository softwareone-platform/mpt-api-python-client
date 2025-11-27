from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateMixin,
    AsyncDeleteMixin,
    AsyncGetMixin,
    CollectionMixin,
    CreateMixin,
    DeleteMixin,
    GetMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import ResourceData


class AccountsUserGroup(Model):
    """Account User Group Model."""


class AccountsUserGroupsServiceConfig:
    """Account User Groups Service Configuration."""

    _endpoint = "/public/v1/accounts/{account_id}/users/{user_id}/groups"
    _model_class = AccountsUserGroup
    _collection_key = "data"


class AccountsUserGroupsService(
    GetMixin[AccountsUserGroup],
    CreateMixin[AccountsUserGroup],
    DeleteMixin,
    CollectionMixin[AccountsUserGroup],
    Service[AccountsUserGroup],
    AccountsUserGroupsServiceConfig,
):
    """Account User Groups Service."""

    def update(self, resource_data: ResourceData) -> AccountsUserGroup:
        """Update Account User Group.

        Args:
            resource_data (ResourceData): Resource data to update.

        Returns:
            AccountsUserGroup: Updated Account User Group.
        """
        response = self.http_client.request("put", self.path, json=resource_data)

        return self._model_class.from_response(response)


class AsyncAccountsUserGroupsService(
    AsyncGetMixin[AccountsUserGroup],
    AsyncCreateMixin[AccountsUserGroup],
    AsyncDeleteMixin,
    AsyncCollectionMixin[AccountsUserGroup],
    AsyncService[AccountsUserGroup],
    AccountsUserGroupsServiceConfig,
):
    """Asynchronous Account User Groups Service."""

    async def update(self, resource_data: ResourceData) -> AccountsUserGroup:
        """Update Account User Group.

        Args:
            resource_data (ResourceData): Resource data to update.

        Returns:
            AccountsUserGroup: Updated Account User Group.
        """
        response = await self.http_client.request("put", self.path, json=resource_data)

        return self._model_class.from_response(response)

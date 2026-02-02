from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.accounts.accounts_user_groups import (
    AccountsUserGroupsService,
    AsyncAccountsUserGroupsService,
)
from mpt_api_client.resources.accounts.mixins import (
    AsyncInvitableMixin,
    InvitableMixin,
)


class AccountsUser(Model):
    """Account User Model."""


class AccountsUsersServiceConfig:
    """Account Users Service Configuration."""

    _endpoint = "/public/v1/accounts/{account_id}/users"
    _model_class = AccountsUser
    _collection_key = "data"


class AccountsUsersService(
    ManagedResourceMixin[AccountsUser],
    InvitableMixin[AccountsUser],
    CollectionMixin[AccountsUser],
    Service[AccountsUser],
    AccountsUsersServiceConfig,
):
    """Account Users Service."""

    def groups(self, user_id: str) -> AccountsUserGroupsService:
        """Return account user groups service."""
        return AccountsUserGroupsService(
            http_client=self.http_client,
            endpoint_params={
                "account_id": self.endpoint_params["account_id"],
                "user_id": user_id,
            },
        )


class AsyncAccountsUsersService(
    AsyncManagedResourceMixin[AccountsUser],
    AsyncInvitableMixin[AccountsUser],
    AsyncCollectionMixin[AccountsUser],
    AsyncService[AccountsUser],
    AccountsUsersServiceConfig,
):
    """Asynchronous Account Users Service."""

    def groups(self, user_id: str) -> AsyncAccountsUserGroupsService:
        """Return account user groups service."""
        return AsyncAccountsUserGroupsService(
            http_client=self.http_client,
            endpoint_params={
                "account_id": self.endpoint_params["account_id"],
                "user_id": user_id,
            },
        )

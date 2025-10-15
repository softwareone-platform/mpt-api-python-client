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
    UpdateMixin[AccountsUser],
    DeleteMixin,
    CreateMixin[AccountsUser],
    InvitableMixin[AccountsUser],
    GetMixin[AccountsUser],
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
    AsyncUpdateMixin[AccountsUser],
    AsyncDeleteMixin,
    AsyncCreateMixin[AccountsUser],
    AsyncInvitableMixin[AccountsUser],
    AsyncGetMixin[AccountsUser],
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

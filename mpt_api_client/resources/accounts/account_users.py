from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateMixin,
    AsyncGetMixin,
    CollectionMixin,
    CreateMixin,
    GetMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.accounts.account_user_groups import (
    AccountUserGroupsService,
    AsyncAccountUserGroupsService,
)
from mpt_api_client.resources.accounts.mixins import (
    AsyncInvitableMixin,
    InvitableMixin,
)


class AccountUser(Model):
    """Account User Model."""


class AccountUsersServiceConfig:
    """Account Users Service Configuration."""

    _endpoint = "/public/v1/accounts/account-users"
    _model_class = AccountUser
    _collection_key = "data"


class AccountUsersService(
    CreateMixin[AccountUser],
    InvitableMixin[AccountUser],
    GetMixin[AccountUser],
    CollectionMixin[AccountUser],
    Service[AccountUser],
    AccountUsersServiceConfig,
):
    """Account Users Service."""

    def groups(self, account_user_id: str) -> AccountUserGroupsService:
        """Return account user groups service."""
        return AccountUserGroupsService(
            http_client=self.http_client,
            endpoint_params={"account_user_id": account_user_id},
        )


class AsyncAccountUsersService(
    AsyncCreateMixin[AccountUser],
    AsyncInvitableMixin[AccountUser],
    AsyncGetMixin[AccountUser],
    AsyncCollectionMixin[AccountUser],
    AsyncService[AccountUser],
    AccountUsersServiceConfig,
):
    """Asynchronous Account Users Service."""

    def groups(self, account_user_id: str) -> AsyncAccountUserGroupsService:
        """Return account user groups service."""
        return AsyncAccountUserGroupsService(
            http_client=self.http_client,
            endpoint_params={"account_user_id": account_user_id},
        )

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateMixin,
    AsyncGetMixin,
    AsyncUpdateMixin,
    CollectionMixin,
    CreateMixin,
    GetMixin,
    UpdateMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.accounts.accounts_users import (
    AccountsUsersService,
    AsyncAccountsUsersService,
)
from mpt_api_client.resources.accounts.mixins import (
    ActivatableMixin,
    AsyncActivatableMixin,
    AsyncEnablableMixin,
    AsyncValidateMixin,
    EnablableMixin,
    ValidateMixin,
)


class Account(Model):
    """Account resource."""


class AccountsServiceConfig:
    """Accounts service configuration."""

    _endpoint = "/public/v1/accounts"
    _model_class = Account
    _collection_key = "data"


class AccountsService(
    CreateMixin[Account],
    UpdateMixin[Account],
    ActivatableMixin[Account],
    EnablableMixin[Account],
    ValidateMixin[Account],
    GetMixin[Account],
    CollectionMixin[Account],
    Service[Account],
    AccountsServiceConfig,
):
    """Accounts service."""

    def users(self, account_id: str) -> AccountsUsersService:
        """Return account users service."""
        return AccountsUsersService(
            http_client=self.http_client, endpoint_params={"account_id": account_id}
        )


class AsyncAccountsService(
    AsyncCreateMixin[Account],
    AsyncUpdateMixin[Account],
    AsyncActivatableMixin[Account],
    AsyncEnablableMixin[Account],
    AsyncValidateMixin[Account],
    AsyncGetMixin[Account],
    AsyncCollectionMixin[Account],
    AsyncService[Account],
    AccountsServiceConfig,
):
    """Async Accounts service."""

    def users(self, account_id: str) -> AsyncAccountsUsersService:
        """Return account users service."""
        return AsyncAccountsUsersService(
            http_client=self.http_client, endpoint_params={"account_id": account_id}
        )

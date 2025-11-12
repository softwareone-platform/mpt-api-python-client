from typing import override

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateWithIconMixin,
    AsyncGetMixin,
    AsyncUpdateWithIconMixin,
    CollectionMixin,
    CreateWithIconMixin,
    GetMixin,
    UpdateWithIconMixin,
)
from mpt_api_client.http.types import FileTypes
from mpt_api_client.models import Model
from mpt_api_client.models.model import ResourceData
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

    _endpoint = "/public/v1/accounts/accounts"
    _model_class = Account
    _collection_key = "data"


class AccountsService(
    CreateWithIconMixin[Account],
    UpdateWithIconMixin[Account],
    ActivatableMixin[Account],
    EnablableMixin[Account],
    ValidateMixin[Account],
    GetMixin[Account],
    CollectionMixin[Account],
    Service[Account],
    AccountsServiceConfig,
):
    """Accounts service."""

    @override
    def create(
        self,
        resource_data: ResourceData,
        logo: FileTypes,
        data_key: str = "account",
        icon_key: str = "logo",
    ) -> Account:
        """
        Create a new account with logo.

        Args:
            resource_data (ResourceData): Account data.
            logo: Logo image in jpg, png, GIF, etc.
            data_key: Key for the account data.
            icon_key: Key for the logo.

        Returns:
            Account: The created account.
        """
        return super().create(
            resource_data=resource_data,
            icon=logo,
            data_key=data_key,
            icon_key=icon_key,
        )

    @override
    def update(
        self,
        resource_id: str,
        resource_data: ResourceData,
        logo: FileTypes,
        data_key: str = "account",
        icon_key: str = "logo",
    ) -> Account:
        """
        Update an existing account with logo.

        Args:
            resource_id (str): The ID of the account to update.
            resource_data (ResourceData): Account data.
            logo: Logo image in jpg, png, GIF, etc.
            data_key: Key for the account data.
            icon_key: Key for the logo.

        Returns:
            Account: The updated account.
        """
        return super().update(
            resource_id=resource_id,
            resource_data=resource_data,
            icon=logo,
            data_key=data_key,
            icon_key=icon_key,
        )

    def users(self, account_id: str) -> AccountsUsersService:
        """Return account users service."""
        return AccountsUsersService(
            http_client=self.http_client, endpoint_params={"account_id": account_id}
        )


class AsyncAccountsService(
    AsyncCreateWithIconMixin[Account],
    AsyncUpdateWithIconMixin[Account],
    AsyncActivatableMixin[Account],
    AsyncEnablableMixin[Account],
    AsyncValidateMixin[Account],
    AsyncGetMixin[Account],
    AsyncCollectionMixin[Account],
    AsyncService[Account],
    AccountsServiceConfig,
):
    """Async Accounts service."""

    @override
    async def create(
        self,
        resource_data: ResourceData,
        logo: FileTypes,
        data_key: str = "account",
        icon_key: str = "logo",
    ) -> Account:
        """
        Create a new account with logo.

        Args:
            resource_data (ResourceData): Account data.
            logo: Logo image in jpg, png, GIF, etc.
            data_key: Key for the account data.
            icon_key: Key for the logo.

        Returns:
            Account: The created account.
        """
        return await super().create(
            resource_data=resource_data,
            icon=logo,
            data_key=data_key,
            icon_key=icon_key,
        )

    @override
    async def update(
        self,
        resource_id: str,
        resource_data: ResourceData,
        logo: FileTypes,
        data_key: str = "account",
        icon_key: str = "logo",
    ) -> Account:
        """
        Update an existing account with logo.

        Args:
            resource_id (str): The ID of the account to update.
            resource_data (ResourceData): Account data.
            logo: Logo image in jpg, png, GIF, etc.
            data_key: Key for the account data.
            icon_key: Key for the logo.

        Returns:
            Account: The updated account.
        """
        return await super().update(
            resource_id=resource_id,
            resource_data=resource_data,
            icon=logo,
            data_key=data_key,
            icon_key=icon_key,
        )

    def users(self, account_id: str) -> AsyncAccountsUsersService:
        """Return account users service."""
        return AsyncAccountsUsersService(
            http_client=self.http_client, endpoint_params={"account_id": account_id}
        )

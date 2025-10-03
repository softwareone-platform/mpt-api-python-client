from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources.accounts.account import AccountsService, AsyncAccountsService
from mpt_api_client.resources.accounts.account_users import (
    AccountUsersService,
    AsyncAccountUsersService,
)
from mpt_api_client.resources.accounts.api_tokens import ApiTokensService, AsyncApiTokensService
from mpt_api_client.resources.accounts.buyers import AsyncBuyersService, BuyersService
from mpt_api_client.resources.accounts.cloud_tenants import (
    AsyncCloudTenantsService,
    CloudTenantsService,
)
from mpt_api_client.resources.accounts.erp_links import AsyncErpLinksService, ErpLinksService
from mpt_api_client.resources.accounts.licensees import AsyncLicenseesService, LicenseesService
from mpt_api_client.resources.accounts.modules import AsyncModulesService, ModulesService
from mpt_api_client.resources.accounts.sellers import AsyncSellersService, SellersService
from mpt_api_client.resources.accounts.user_groups import (
    AsyncUserGroupsService,
    UserGroupsService,
)
from mpt_api_client.resources.accounts.users import AsyncUsersService, UsersService


class Accounts:
    """Accounts MPT API Module."""

    def __init__(self, *, http_client: HTTPClient):
        self.http_client = http_client

    @property
    def accounts(self) -> AccountsService:
        """Accounts service."""
        return AccountsService(http_client=self.http_client)

    @property
    def users(self) -> UsersService:
        """Users service."""
        return UsersService(http_client=self.http_client)

    @property
    def sellers(self) -> SellersService:
        """Sellers service."""
        return SellersService(http_client=self.http_client)

    @property
    def licensees(self) -> LicenseesService:
        """Licensees service."""
        return LicenseesService(http_client=self.http_client)

    @property
    def user_groups(self) -> UserGroupsService:
        """User Groups service."""
        return UserGroupsService(http_client=self.http_client)

    @property
    def api_tokens(self) -> ApiTokensService:
        """API Tokens service."""
        return ApiTokensService(http_client=self.http_client)

    @property
    def modules(self) -> ModulesService:
        """Modules service."""
        return ModulesService(http_client=self.http_client)

    @property
    def cloud_tenants(self) -> CloudTenantsService:
        """Cloud Tenants service."""
        return CloudTenantsService(http_client=self.http_client)

    @property
    def buyers(self) -> BuyersService:
        """Buyers service."""
        return BuyersService(http_client=self.http_client)

    @property
    def account_users(self) -> AccountUsersService:
        """Account Users service."""
        return AccountUsersService(http_client=self.http_client)

    @property
    def erp_links(self) -> ErpLinksService:
        """ERP Links service."""
        return ErpLinksService(http_client=self.http_client)


class AsyncAccounts:
    """Async Accounts MPT API Module."""

    def __init__(self, *, http_client: AsyncHTTPClient):
        self.http_client = http_client

    @property
    def accounts(self) -> AsyncAccountsService:
        """Accounts service."""
        return AsyncAccountsService(http_client=self.http_client)

    @property
    def users(self) -> AsyncUsersService:
        """Users service."""
        return AsyncUsersService(http_client=self.http_client)

    @property
    def sellers(self) -> AsyncSellersService:
        """Sellers service."""
        return AsyncSellersService(http_client=self.http_client)

    @property
    def licensees(self) -> AsyncLicenseesService:
        """Licensees service."""
        return AsyncLicenseesService(http_client=self.http_client)

    @property
    def user_groups(self) -> AsyncUserGroupsService:
        """User Groups service."""
        return AsyncUserGroupsService(http_client=self.http_client)

    @property
    def api_tokens(self) -> AsyncApiTokensService:
        """API Tokens service."""
        return AsyncApiTokensService(http_client=self.http_client)

    @property
    def modules(self) -> AsyncModulesService:
        """Modules service."""
        return AsyncModulesService(http_client=self.http_client)

    @property
    def cloud_tenants(self) -> AsyncCloudTenantsService:
        """Cloud Tenants service."""
        return AsyncCloudTenantsService(http_client=self.http_client)

    @property
    def buyers(self) -> AsyncBuyersService:
        """Buyers service."""
        return AsyncBuyersService(http_client=self.http_client)

    @property
    def account_users(self) -> AsyncAccountUsersService:
        """Account Users service."""
        return AsyncAccountUsersService(http_client=self.http_client)

    @property
    def erp_links(self) -> AsyncErpLinksService:
        """ERP Links service."""
        return AsyncErpLinksService(http_client=self.http_client)

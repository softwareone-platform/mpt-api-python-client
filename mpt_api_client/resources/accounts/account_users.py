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
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.accounts.mixins import (
    AsyncInvitableMixin,
    InvitableMixin,
)


class AccountUser(Model):
    """Account User resource.

    Attributes:
        user: Reference to the platform user.
        account: Reference to the account the user belongs to.
        groups: User groups the account user belongs to.
        buyers: Buyers the account user is scoped to.
        modules: Modules the account user has access to.
        invitation: Invitation details for the account user.
        last_login_at: Timestamp of the last successful login.
        audit: Audit information.
    """

    user: BaseModel | None
    account: BaseModel | None
    groups: list[BaseModel] | None
    buyers: list[BaseModel] | None
    modules: list[BaseModel] | None
    invitation: BaseModel | None
    last_login_at: str | None
    audit: BaseModel | None


class AccountUsersServiceConfig:
    """Account Users Service Configuration."""

    _endpoint = "/public/v1/accounts/account-users"
    _model_class = AccountUser
    _collection_key = "data"


class AccountUsersService(
    CreateMixin[AccountUser],
    GetMixin[AccountUser],
    DeleteMixin,
    InvitableMixin[AccountUser],
    CollectionMixin[AccountUser],
    Service[AccountUser],
    AccountUsersServiceConfig,
):
    """Account Users Service."""


class AsyncAccountUsersService(
    AsyncCreateMixin[AccountUser],
    AsyncGetMixin[AccountUser],
    AsyncDeleteMixin,
    AsyncInvitableMixin[AccountUser],
    AsyncCollectionMixin[AccountUser],
    AsyncService[AccountUser],
    AccountUsersServiceConfig,
):
    """Asynchronous Account Users Service."""

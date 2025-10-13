from typing import override

from mpt_api_client.exceptions import MPTError
from mpt_api_client.http import AsyncService, Service
from mpt_api_client.models import Model


class MethodNotAllowedError(MPTError):
    """Method not allowed error."""


class Contact(Model):
    """Account resource."""


class AccountsServiceConfig:
    """Accounts service config."""

    _endpoint = "/public/v1/commerce/accounts/{account_id}/categories/{category_id}/contacts"
    _model_class = Contact
    _collection_key = "data"


class AccountsService(Service[Contact], AccountsServiceConfig):
    """Accounts service."""

    @override
    def get(self, resource_id: str, select: list[str] | str | None = None) -> Contact:
        # TODO: delete. This method does not exist in the api
        raise MethodNotAllowedError("Operation not allowed")


class AsyncAccountsService(AsyncService[Contact], AccountsServiceConfig):
    """Async Accounts service."""

    @override
    async def get(self, resource_id: str, select: list[str] | str | None = None) -> Contact:
        # TODO: delete. This method does not exist in the api
        raise MethodNotAllowedError("Operation not allowed")

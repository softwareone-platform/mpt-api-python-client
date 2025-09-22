from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources.catalog.authorizations import (
    AsyncAuthorizationsService,
    AuthorizationsService,
)
from mpt_api_client.resources.catalog.items import AsyncItemsService, ItemsService
from mpt_api_client.resources.catalog.price_list_items import (
    AsyncPriceListItemsService,
    PriceListItemsService,
)
from mpt_api_client.resources.catalog.price_lists import (
    AsyncPriceListsService,
    PriceListsService,
)
from mpt_api_client.resources.catalog.products import AsyncProductsService, ProductsService


class Catalog:
    """Catalog MPT API Module."""

    def __init__(self, *, http_client: HTTPClient):
        self.http_client = http_client

    @property
    def authorizations(self) -> AuthorizationsService:
        """Authorizations service."""
        return AuthorizationsService(http_client=self.http_client)

    def price_list_items(self, price_list_id: str) -> PriceListItemsService:
        """Price List Items service."""
        return PriceListItemsService(
            http_client=self.http_client, endpoint_params={"price_list_id": price_list_id}
        )

    @property
    def price_lists(self) -> PriceListsService:
        """Price Lists service."""
        return PriceListsService(http_client=self.http_client)

    @property
    def products(self) -> ProductsService:
        """Products service."""
        return ProductsService(http_client=self.http_client)

    @property
    def items(self) -> ItemsService:  # noqa: WPS110
        """Items service."""
        return ItemsService(http_client=self.http_client)


class AsyncCatalog:
    """Catalog MPT API Module."""

    def __init__(self, *, http_client: AsyncHTTPClient):
        self.http_client = http_client

    @property
    def authorizations(self) -> AsyncAuthorizationsService:
        """Authorizations service."""
        return AsyncAuthorizationsService(http_client=self.http_client)

    def price_list_items(self, price_list_id: str) -> AsyncPriceListItemsService:
        """Price List Items service."""
        return AsyncPriceListItemsService(
            http_client=self.http_client, endpoint_params={"price_list_id": price_list_id}
        )

    @property
    def price_lists(self) -> AsyncPriceListsService:
        """Price Lists service."""
        return AsyncPriceListsService(http_client=self.http_client)

    @property
    def products(self) -> AsyncProductsService:
        """Products service."""
        return AsyncProductsService(http_client=self.http_client)

    @property
    def items(self) -> AsyncItemsService:  # noqa: WPS110
        """Items service."""
        return AsyncItemsService(http_client=self.http_client)

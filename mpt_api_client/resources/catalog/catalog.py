from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources.catalog.authorizations import (
    AsyncAuthorizationsService,
    AuthorizationsService,
)
from mpt_api_client.resources.catalog.items import AsyncItemsService, ItemsService
from mpt_api_client.resources.catalog.listings import AsyncListingsService, ListingsService
from mpt_api_client.resources.catalog.price_lists import (
    AsyncPriceListsService,
    PriceListsService,
)
from mpt_api_client.resources.catalog.pricing_policies import (
    AsyncPricingPoliciesService,
    PricingPoliciesService,
)
from mpt_api_client.resources.catalog.products import AsyncProductsService, ProductsService
from mpt_api_client.resources.catalog.units_of_measure import (
    AsyncUnitsOfMeasureService,
    UnitsOfMeasureService,
)


class Catalog:
    """Catalog MPT API Module."""

    def __init__(self, *, http_client: HTTPClient):
        self.http_client = http_client

    @property
    def authorizations(self) -> AuthorizationsService:
        """Authorizations service."""
        return AuthorizationsService(http_client=self.http_client)

    @property
    def listings(self) -> ListingsService:
        """Listings service."""
        return ListingsService(http_client=self.http_client)

    @property
    def price_lists(self) -> PriceListsService:
        """Price Lists service."""
        return PriceListsService(http_client=self.http_client)

    @property
    def pricing_policies(self) -> PricingPoliciesService:
        """Pricing policies service."""
        return PricingPoliciesService(http_client=self.http_client)

    @property
    def products(self) -> ProductsService:
        """Products service."""
        return ProductsService(http_client=self.http_client)

    @property
    def units_of_measure(self) -> UnitsOfMeasureService:
        """Units of Measure service."""
        return UnitsOfMeasureService(http_client=self.http_client)

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

    @property
    def listings(self) -> AsyncListingsService:
        """Listings service."""
        return AsyncListingsService(http_client=self.http_client)

    @property
    def price_lists(self) -> AsyncPriceListsService:
        """Price Lists service."""
        return AsyncPriceListsService(http_client=self.http_client)

    @property
    def pricing_policies(self) -> AsyncPricingPoliciesService:
        """Pricing policies service."""
        return AsyncPricingPoliciesService(http_client=self.http_client)

    @property
    def products(self) -> AsyncProductsService:
        """Products service."""
        return AsyncProductsService(http_client=self.http_client)

    @property
    def units_of_measure(self) -> AsyncUnitsOfMeasureService:
        """Units of Measure service."""
        return AsyncUnitsOfMeasureService(http_client=self.http_client)

    @property
    def items(self) -> AsyncItemsService:  # noqa: WPS110
        """Items service."""
        return AsyncItemsService(http_client=self.http_client)

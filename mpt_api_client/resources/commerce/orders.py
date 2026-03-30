from mpt_api_client.http import (
    AsyncService,
    Service,
)
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model, ResourceData
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.commerce.mixins import (
    AsyncRenderMixin,
    AsyncTemplateMixin,
    RenderMixin,
    TemplateMixin,
)
from mpt_api_client.resources.commerce.orders_asset import (
    AsyncOrdersAssetService,
    OrdersAssetService,
)
from mpt_api_client.resources.commerce.orders_subscription import (
    AsyncOrderSubscriptionsService,
    OrderSubscriptionsService,
)


class Order(Model):
    """Order resource.

    Attributes:
        type: Order type.
        status: Order status.
        notes: Order notes.
        comments: Order comments.
        default_markup_source: Default markup source.
        status_notes: Status notes details.
        template: Reference to the template.
        listing: Reference to the listing.
        authorization: Reference to the authorization.
        agreement: Reference to the agreement.
        assignee: Reference to the assignee.
        external_ids: External identifiers.
        price: Price information.
        lines: List of order lines.
        subscriptions: List of subscriptions.
        assets: List of assets.
        parameters: Order parameters.
        error: Error information.
        product: Reference to the product.
        client: Reference to the client account.
        licensee: Reference to the licensee.
        buyer: Reference to the buyer.
        seller: Reference to the seller.
        vendor: Reference to the vendor account.
        bill_to: Bill-to address.
        pricing_policy: Reference to the pricing policy.
        terms_and_conditions: List of terms and conditions.
        certificates: List of certificates.
        audit: Audit information.
    """

    type: str | None
    status: str | None
    notes: str | None
    comments: str | None
    default_markup_source: str | None
    status_notes: BaseModel | None
    template: BaseModel | None
    listing: BaseModel | None
    authorization: BaseModel | None
    agreement: BaseModel | None
    assignee: BaseModel | None
    external_ids: BaseModel | None
    price: BaseModel | None
    lines: list[BaseModel] | None
    subscriptions: list[BaseModel] | None
    assets: list[BaseModel] | None
    parameters: BaseModel | None  # noqa: WPS110
    error: BaseModel | None
    product: BaseModel | None
    client: BaseModel | None
    licensee: BaseModel | None
    buyer: BaseModel | None
    seller: BaseModel | None
    vendor: BaseModel | None
    bill_to: BaseModel | None
    pricing_policy: BaseModel | None
    terms_and_conditions: list[BaseModel] | None
    certificates: list[BaseModel] | None
    audit: BaseModel | None


class OrdersServiceConfig:
    """Orders service config."""

    _endpoint = "/public/v1/commerce/orders"
    _model_class = Order
    _collection_key = "data"


class OrdersService(  # noqa: WPS215 WPS214
    RenderMixin[Order],
    TemplateMixin[Order],
    ManagedResourceMixin[Order],
    CollectionMixin[Order],
    Service[Order],
    OrdersServiceConfig,
):
    """Orders service."""

    def validate(self, resource_id: str, resource_data: ResourceData | None = None) -> Order:
        """Switch order to validate state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated
        """
        return self._resource(resource_id).post("validate", json=resource_data)

    def process(self, resource_id: str, resource_data: ResourceData | None = None) -> Order:
        """Switch order to process state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated
        """
        return self._resource(resource_id).post("process", json=resource_data)

    def query(self, resource_id: str, resource_data: ResourceData | None = None) -> Order:
        """Switch order to query state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated
        """
        return self._resource(resource_id).post("query", json=resource_data)

    def complete(self, resource_id: str, resource_data: ResourceData | None = None) -> Order:
        """Switch order to complete state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated
        """
        return self._resource(resource_id).post("complete", json=resource_data)

    def fail(self, resource_id: str, resource_data: ResourceData | None = None) -> Order:
        """Switch order to fail state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated
        """
        return self._resource(resource_id).post("fail", json=resource_data)

    def notify(self, resource_id: str, user: ResourceData) -> None:
        """Notify user about order status.

        Args:
            resource_id: Order resource ID
            user: User data
        """
        self._resource(resource_id).do_request("POST", "notify", json=user)

    def quote(self, resource_id: str, resource_data: ResourceData | None = None) -> Order:
        """Quote the order.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated

        Returns:
            Quoted order resource.
        """
        return self._resource(resource_id).post("quote", json=resource_data)

    def subscriptions(self, order_id: str) -> OrderSubscriptionsService:
        """Get the subscription service for the given Order id.

        Args:
            order_id: Order ID.

        Returns:
            Order Subscription service.
        """
        return OrderSubscriptionsService(
            http_client=self.http_client,
            endpoint_params={"order_id": order_id},
        )

    def assets(self, order_id: str) -> OrdersAssetService:
        """Get the asset service for the given Order id.

        Args:
            order_id: Order ID.

        Returns:
            Order Asset service.
        """
        return OrdersAssetService(
            http_client=self.http_client,
            endpoint_params={"order_id": order_id},
        )


class AsyncOrdersService(  # noqa: WPS215 WPS214
    AsyncRenderMixin[Order],
    AsyncTemplateMixin[Order],
    AsyncManagedResourceMixin[Order],
    AsyncCollectionMixin[Order],
    AsyncService[Order],
    OrdersServiceConfig,
):
    """Async Orders service."""

    async def validate(self, resource_id: str, resource_data: ResourceData | None = None) -> Order:
        """Switch order to validate state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated

        Returns:
            Updated order resource
        """
        return await self._resource(resource_id).post("validate", json=resource_data)

    async def process(self, resource_id: str, resource_data: ResourceData | None = None) -> Order:
        """Switch order to process state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated

        Returns:
            Updated order resource
        """
        return await self._resource(resource_id).post("process", json=resource_data)

    async def query(self, resource_id: str, resource_data: ResourceData | None = None) -> Order:
        """Switch order to query state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated

        Returns:
            Updated order resource
        """
        return await self._resource(resource_id).post("query", json=resource_data)

    async def complete(self, resource_id: str, resource_data: ResourceData | None = None) -> Order:
        """Switch order to complete state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated

        Returns:
            Updated order resource
        """
        return await self._resource(resource_id).post("complete", json=resource_data)

    async def fail(self, resource_id: str, resource_data: ResourceData | None = None) -> Order:
        """Switch order to fail state.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated

        Returns:
            Updated order resource
        """
        return await self._resource(resource_id).post("fail", json=resource_data)

    async def notify(self, resource_id: str, resource_data: ResourceData) -> None:
        """Notify user about order status.

        Args:
            resource_id: Order resource ID
            resource_data: User data to notify
        """
        await self._resource(resource_id).do_request("POST", "notify", json=resource_data)

    async def quote(self, resource_id: str, resource_data: ResourceData | None = None) -> Order:
        """Quote the order.

        Args:
            resource_id: Order resource ID
            resource_data: Order data will be updated

        Returns:
            Quoted order resource.
        """
        return await self._resource(resource_id).post("quote", json=resource_data)

    def subscriptions(self, order_id: str) -> AsyncOrderSubscriptionsService:
        """Get the subscription service for the given Order id.

        Args:
            order_id: Order ID.

        Returns:
            Order Subscription service.
        """
        return AsyncOrderSubscriptionsService(
            http_client=self.http_client,
            endpoint_params={"order_id": order_id},
        )

    def assets(self, order_id: str) -> AsyncOrdersAssetService:
        """Get the asset service for the given Order id.

        Args:
            order_id: Order ID.

        Returns:
            Order Asset service.
        """
        return AsyncOrdersAssetService(
            http_client=self.http_client,
            endpoint_params={"order_id": order_id},
        )

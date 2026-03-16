from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel


class OrderSubscription(Model):
    """Order Subscription resource.

    Attributes:
        name: Subscription name.
        status: Subscription status.
        start_date: Subscription start date.
        termination_date: Subscription termination date.
        commitment_date: Subscription commitment date.
        auto_renew: Whether the subscription auto-renews.
        external_ids: External identifiers.
        terms: Reference to terms and conditions.
        product: Reference to the product.
        parameters: Subscription parameters.
        agreement: Reference to the agreement.
        price: Price information.
        template: Reference to the template.
        lines: List of subscription lines.
        audit: Audit information.
    """

    name: str | None
    status: str | None
    start_date: str | None
    termination_date: str | None
    commitment_date: str | None
    auto_renew: bool | None
    external_ids: BaseModel | None
    terms: BaseModel | None
    product: BaseModel | None
    parameters: BaseModel | None  # noqa: WPS110
    agreement: BaseModel | None
    price: BaseModel | None
    template: BaseModel | None
    lines: list[BaseModel] | None
    audit: BaseModel | None


class OrderSubscriptionsServiceConfig:
    """Orders service config."""

    _endpoint = "/public/v1/commerce/orders/{order_id}/subscriptions"
    _model_class = OrderSubscription
    _collection_key = "data"


class OrderSubscriptionsService(  # noqa: WPS215
    ManagedResourceMixin[OrderSubscription],
    CollectionMixin[OrderSubscription],
    Service[OrderSubscription],
    OrderSubscriptionsServiceConfig,
):
    """Orders Subscription service."""


class AsyncOrderSubscriptionsService(  # noqa: WPS215
    AsyncManagedResourceMixin[OrderSubscription],
    AsyncCollectionMixin[OrderSubscription],
    AsyncService[OrderSubscription],
    OrderSubscriptionsServiceConfig,
):
    """Async Orders Subscription service."""

from mpt_api_client.http import (
    AsyncService,
    Service,
)
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
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.commerce.mixins import (
    AsyncRenderMixin,
    AsyncTerminateMixin,
    RenderMixin,
    TerminateMixin,
)


class Subscription(Model):
    """Subscription resource.

    Attributes:
        name: Subscription name.
        status: Subscription status.
        start_date: Subscription start date.
        termination_date: Subscription termination date.
        commitment_date: Subscription commitment date.
        split_status: Split billing status.
        auto_renew: Whether the subscription auto-renews.
        external_ids: External identifiers.
        terms: Reference to terms and conditions.
        product: Reference to the product.
        price: Price information.
        parameters: Subscription parameters.
        agreement: Reference to the agreement.
        buyer: Reference to the buyer.
        licensee: Reference to the licensee.
        seller: Reference to the seller.
        split: Split billing information.
        template: Reference to the template.
        lines: List of subscription lines.
        audit: Audit information.
    """

    name: str | None
    status: str | None
    start_date: str | None
    termination_date: str | None
    commitment_date: str | None
    split_status: str | None
    auto_renew: bool | None
    external_ids: BaseModel | None
    terms: BaseModel | None
    product: BaseModel | None
    price: BaseModel | None
    parameters: BaseModel | None  # noqa: WPS110
    agreement: BaseModel | None
    buyer: BaseModel | None
    licensee: BaseModel | None
    seller: BaseModel | None
    split: BaseModel | None
    template: BaseModel | None
    lines: list[BaseModel] | None
    audit: BaseModel | None


class SubscriptionsServiceConfig:
    """Subscription service config."""

    _endpoint = "/public/v1/commerce/subscriptions"
    _model_class = Subscription
    _collection_key = "data"


class SubscriptionsService(  # noqa: WPS215
    CreateMixin[Subscription],
    UpdateMixin[Subscription],
    GetMixin[Subscription],
    CollectionMixin[Subscription],
    TerminateMixin[Subscription],
    RenderMixin[Subscription],
    Service[Subscription],
    SubscriptionsServiceConfig,
):
    """Subscription service."""


class AsyncSubscriptionsService(  # noqa: WPS215
    AsyncCreateMixin[Subscription],
    AsyncUpdateMixin[Subscription],
    AsyncGetMixin[Subscription],
    AsyncCollectionMixin[Subscription],
    AsyncTerminateMixin[Subscription],
    AsyncRenderMixin[Subscription],
    AsyncService[Subscription],
    SubscriptionsServiceConfig,
):
    """Async Subscription service."""

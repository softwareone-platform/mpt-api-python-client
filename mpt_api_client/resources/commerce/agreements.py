from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.commerce.agreements_attachments import (
    AgreementsAttachmentService,
    AsyncAgreementsAttachmentService,
)
from mpt_api_client.resources.commerce.mixins import (
    AsyncRenderMixin,
    AsyncTemplateMixin,
    RenderMixin,
    TemplateMixin,
)


class Agreement(Model):
    """Agreement resource.

    Attributes:
        icon: URL or identifier for the agreement icon.
        status: Agreement status.
        name: Agreement name.
        start_date: Agreement start date.
        end_date: Agreement end date.
        listing: Reference to the listing.
        authorization: Reference to the authorization.
        vendor: Reference to the vendor account.
        client: Reference to the client account.
        price: Price information.
        template: Reference to the template.
        error: Error information.
        lines: List of agreement lines.
        assets: List of assets.
        subscriptions: List of subscriptions.
        parameters: Agreement parameters.
        licensee: Reference to the licensee.
        buyer: Reference to the buyer.
        seller: Reference to the seller.
        product: Reference to the product.
        external_ids: External identifiers.
        split: Split billing information.
        terms_and_conditions: List of terms and conditions.
        certificates: List of certificates.
        audit: Audit information.
    """

    icon: str | None
    status: str | None
    name: str | None
    start_date: str | None
    end_date: str | None
    listing: BaseModel | None
    authorization: BaseModel | None
    vendor: BaseModel | None
    client: BaseModel | None
    price: BaseModel | None
    template: BaseModel | None
    error: BaseModel | None
    lines: list[BaseModel] | None
    assets: list[BaseModel] | None
    subscriptions: list[BaseModel] | None
    parameters: BaseModel | None  # noqa: WPS110
    licensee: BaseModel | None
    buyer: BaseModel | None
    seller: BaseModel | None
    product: BaseModel | None
    external_ids: BaseModel | None
    split: BaseModel | None
    terms_and_conditions: list[BaseModel] | None
    certificates: list[BaseModel] | None
    audit: BaseModel | None


class AgreementsServiceConfig:
    """Orders service config."""

    _endpoint = "/public/v1/commerce/agreements"
    _model_class = Agreement
    _collection_key = "data"


class AgreementsService(
    RenderMixin[Agreement],
    TemplateMixin[Agreement],
    ManagedResourceMixin[Agreement],
    CollectionMixin[Agreement],
    Service[Agreement],
    AgreementsServiceConfig,
):
    """Agreements service."""

    def attachments(self, agreement_id: str) -> AgreementsAttachmentService:
        """Get the attachments service for the given Agreement id.

        Args:
            agreement_id: Agreement ID.

        Returns:
            Agreements Attachment service.
        """
        return AgreementsAttachmentService(
            http_client=self.http_client,
            endpoint_params={"agreement_id": agreement_id},
        )


class AsyncAgreementsService(
    AsyncRenderMixin[Agreement],
    AsyncTemplateMixin[Agreement],
    AsyncManagedResourceMixin[Agreement],
    AsyncCollectionMixin[Agreement],
    AsyncService[Agreement],
    AgreementsServiceConfig,
):
    """Agreements service."""

    def attachments(self, agreement_id: str) -> AsyncAgreementsAttachmentService:
        """Get the attachments service for the given Agreement id.

        Args:
            agreement_id: Agreement ID.

        Returns:
            Agreements Attachment service.
        """
        return AsyncAgreementsAttachmentService(
            http_client=self.http_client,
            endpoint_params={"agreement_id": agreement_id},
        )

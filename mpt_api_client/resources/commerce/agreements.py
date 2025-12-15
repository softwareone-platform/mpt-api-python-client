from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
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
    """Agreement resource."""


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

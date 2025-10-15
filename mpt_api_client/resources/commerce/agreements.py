from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCreateMixin,
    AsyncDeleteMixin,
    AsyncGetMixin,
    AsyncUpdateMixin,
    CreateMixin,
    DeleteMixin,
    GetMixin,
    UpdateMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.commerce.agreements_attachments import (
    AgreementsAttachmentService,
    AsyncAgreementsAttachmentService,
)


class Agreement(Model):
    """Agreement resource."""


class AgreementsServiceConfig:
    """Orders service config."""

    _endpoint = "/public/v1/commerce/agreements"
    _model_class = Agreement
    _collection_key = "data"


class AgreementsService(  # noqa: WPS215
    CreateMixin[Agreement],
    UpdateMixin[Agreement],
    GetMixin[Agreement],
    DeleteMixin,
    Service[Agreement],
    AgreementsServiceConfig,
):
    """Agreements service."""

    def template(self, agreement_id: str) -> str:
        """Renders the template for the given Agreement id.

        Args:
            agreement_id: Agreement ID.

        Returns:
            Agreement template.
        """
        response = self._resource_do_request(agreement_id, action="template")
        return response.text

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


class AsyncAgreementsService(  # noqa: WPS215
    AsyncCreateMixin[Agreement],
    AsyncUpdateMixin[Agreement],
    AsyncGetMixin[Agreement],
    AsyncDeleteMixin,
    AsyncService[Agreement],
    AgreementsServiceConfig,
):
    """Agreements service."""

    async def template(self, agreement_id: str) -> str:
        """Renders the template for the given Agreement id.

        Args:
            agreement_id: Agreement ID.

        Returns:
            Agreement template.
        """
        response = await self._resource_do_request(agreement_id, action="template")
        return response.text

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

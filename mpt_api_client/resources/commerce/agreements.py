from mpt_api_client.http import AsyncService, Service
from mpt_api_client.models import Model


class Agreement(Model):
    """Agreement resource."""


class AgreementsServiceConfig:
    """Orders service config."""

    _endpoint = "/public/v1/commerce/agreements"
    _model_class = Agreement
    _collection_key = "data"


class AgreementsService(Service[Agreement], AgreementsServiceConfig):
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


class AsyncAgreementsService(AsyncService[Agreement], AgreementsServiceConfig):
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

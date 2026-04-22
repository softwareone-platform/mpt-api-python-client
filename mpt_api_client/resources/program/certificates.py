from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel, ResourceData


class Certificate(Model):
    """Program certificate resource.

    Attributes:
        name: Certificate name.
        program: Reference to the program.
        vendor: Reference to the vendor.
        external_ids: External identifiers.
        client: Reference to the client.
        applicable_to: Applicable to which entities.
        licensee: Reference to the licensee.
        eligibility: Eligibility criteria.
        status: Certificate status.
        status_notes: Additional notes on the certificate status.
        parameters: Certificate parameters.
        audit: Audit information.
    """

    name: str | None
    program: BaseModel | None
    vendor: BaseModel | None
    external_ids: BaseModel | None
    client: BaseModel | None
    applicable_to: str | None
    licensee: BaseModel | None
    eligibility: BaseModel | None
    status: str | None
    status_notes: str | None
    parameters: BaseModel | None  # noqa: WPS110
    audit: BaseModel | None


class CertificateServiceConfig:
    """Program certificate service config."""

    _endpoint = "/public/v1/program/certificates"
    _model_class = Certificate
    _collection_key = "data"


class CertificateService(
    ManagedResourceMixin[Certificate],
    CollectionMixin[Certificate],
    Service[Certificate],
    CertificateServiceConfig,
):
    """Program certificate service."""

    def terminate(self, resource_id: str, resource_data: ResourceData | None = None) -> Certificate:
        """Terminate a certificate.

        Args:
            resource_id: Certificate ID.
            resource_data: Additional data for termination.

        Returns:
            Terminated certificate.
        """
        return self._resource(resource_id).post("/terminate", json=resource_data)


class AsyncCertificateService(
    AsyncManagedResourceMixin[Certificate],
    AsyncCollectionMixin[Certificate],
    AsyncService[Certificate],
    CertificateServiceConfig,
):
    """Asynchronous program certificate service."""

    async def terminate(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> Certificate:
        """Asynchronously terminate a certificate.

        Args:
            resource_id: Certificate ID.
            resource_data: Additional data for termination.

        Returns:
            Terminated certificate.
        """
        return await self._resource(resource_id).post("/terminate", json=resource_data)

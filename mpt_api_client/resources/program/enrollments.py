from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel, ResourceData
from mpt_api_client.resources.program.mixins.render_mixin import AsyncRenderMixin, RenderMixin


class Enrollment(Model):
    """Program enrollment resource.

    Attributes:
        name: Enrollment name.
        certificate: Reference to the certificate.
        program: Reference to the program.
        vendor: Reference to the vendor.
        applicable_to: Applicable to which entities.
        type: Enrollment type.
        licensee: Reference to the licensee.
        eligibility: Eligibility criteria.
        status: Enrollment status.
        parameters: Enrollment parameters.
        template: Reference to the enrollment template.
        audit: Audit information.
    """

    name: str | None
    certificate: BaseModel | None
    program: BaseModel | None
    vendor: BaseModel | None
    applicable_to: str | None
    type: str | None
    licensee: BaseModel | None
    eligibility: BaseModel | None
    status: str | None
    parameters: BaseModel | None  # noqa: WPS110
    template: BaseModel | None
    audit: BaseModel | None


class EnrollmentServiceConfig:
    """Program enrollment service config."""

    _endpoint = "/public/v1/program/enrollments"
    _model_class = Enrollment
    _collection_key = "data"


class EnrollmentService(
    RenderMixin[Enrollment],
    ManagedResourceMixin[Enrollment],
    CollectionMixin[Enrollment],
    Service[Enrollment],
    EnrollmentServiceConfig,
):
    """Program enrollment service."""

    def validate(self, resource_id: str, resource_data: ResourceData | None = None) -> Enrollment:
        """Validate enrollment.

        Args:
            resource_id: Enrollment ID
            resource_data: Enrollment data will be validated

        Returns:
            Validated enrollment.
        """
        return self._resource(resource_id).post("validate", json=resource_data)

    def query(self, resource_id: str, resource_data: ResourceData | None = None) -> Enrollment:
        """Query enrollment.

        Args:
            resource_id: Enrollment ID
            resource_data: Enrollment data will be queried

        Returns:
            Queried enrollment.
        """
        return self._resource(resource_id).post("query", json=resource_data)

    def process(self, resource_id: str, resource_data: ResourceData | None = None) -> Enrollment:
        """Process enrollment.

        Args:
            resource_id: Enrollment ID
            resource_data: Enrollment data will be processed

        Returns:
            Processed enrollment.
        """
        return self._resource(resource_id).post("process", json=resource_data)

    def complete(self, resource_id: str, resource_data: ResourceData | None = None) -> Enrollment:
        """Complete enrollment.

        Args:
            resource_id: Enrollment ID
            resource_data: Enrollment data will be completed

        Returns:
            Completed enrollment.
        """
        return self._resource(resource_id).post("complete", json=resource_data)

    def submit(self, resource_id: str, resource_data: ResourceData | None = None) -> Enrollment:
        """Submit enrollment.

        Args:
            resource_id: Enrollment ID
            resource_data: Enrollment data will be submitted

        Returns:
            Submitted enrollment.
        """
        return self._resource(resource_id).post("submit", json=resource_data)

    def fail(self, resource_id: str, resource_data: ResourceData | None = None) -> Enrollment:
        """Fail enrollment.

        Args:
            resource_id: Enrollment ID
            resource_data: Enrollment data will be failed

        Returns:
            Failed enrollment.
        """
        return self._resource(resource_id).post("fail", json=resource_data)


class AsyncEnrollmentService(
    AsyncRenderMixin[Enrollment],
    AsyncManagedResourceMixin[Enrollment],
    AsyncCollectionMixin[Enrollment],
    AsyncService[Enrollment],
    EnrollmentServiceConfig,
):
    """Async program enrollment service."""

    async def validate(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> Enrollment:
        """Validate enrollment.

        Args:
            resource_id: Enrollment ID
            resource_data: Enrollment data will be validated

        Returns:
            Validated enrollment.
        """
        return await self._resource(resource_id).post("validate", json=resource_data)

    async def query(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> Enrollment:
        """Query enrollment.

        Args:
            resource_id: Enrollment ID
            resource_data: Enrollment data will be queried

        Returns:
            Queried enrollment.
        """
        return await self._resource(resource_id).post("query", json=resource_data)

    async def process(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> Enrollment:
        """Process enrollment.

        Args:
            resource_id: Enrollment ID
            resource_data: Enrollment data will be processed

        Returns:
            Processed enrollment.
        """
        return await self._resource(resource_id).post("process", json=resource_data)

    async def complete(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> Enrollment:
        """Complete enrollment.

        Args:
            resource_id: Enrollment ID
            resource_data: Enrollment data will be completed

        Returns:
            Completed enrollment.
        """
        return await self._resource(resource_id).post("complete", json=resource_data)

    async def submit(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> Enrollment:
        """Submit enrollment.

        Args:
            resource_id: Enrollment ID
            resource_data: Enrollment data will be submitted

        Returns:
            Submitted enrollment.
        """
        return await self._resource(resource_id).post("submit", json=resource_data)

    async def fail(self, resource_id: str, resource_data: ResourceData | None = None) -> Enrollment:
        """Fail enrollment.

        Args:
            resource_id: Enrollment ID
            resource_data: Enrollment data will be failed

        Returns:
            Failed enrollment.
        """
        return await self._resource(resource_id).post("fail", json=resource_data)

from mpt_api_client.http import AsyncHTTPClient, HTTPClient
from mpt_api_client.resources.program.certificates import (
    AsyncCertificateService,
    CertificateService,
)
from mpt_api_client.resources.program.enrollments import AsyncEnrollmentService, EnrollmentService
from mpt_api_client.resources.program.programs import AsyncProgramsService, ProgramsService


class Program:
    """Program MPT API Module."""

    def __init__(self, *, http_client: HTTPClient):
        self.http_client = http_client

    @property
    def programs(self) -> ProgramsService:
        """Programs service."""
        return ProgramsService(http_client=self.http_client)

    @property
    def enrollments(self) -> EnrollmentService:
        """Enrollments service."""
        return EnrollmentService(http_client=self.http_client)

    @property
    def certificates(self) -> CertificateService:
        """Certificates service."""
        return CertificateService(http_client=self.http_client)


class AsyncProgram:
    """Program MPT API Module."""

    def __init__(self, *, http_client: AsyncHTTPClient):
        self.http_client = http_client

    @property
    def programs(self) -> AsyncProgramsService:
        """Programs service."""
        return AsyncProgramsService(http_client=self.http_client)

    @property
    def enrollments(self) -> AsyncEnrollmentService:
        """Enrollments service."""
        return AsyncEnrollmentService(http_client=self.http_client)

    @property
    def certificates(self) -> AsyncCertificateService:
        """Certificates service."""
        return AsyncCertificateService(http_client=self.http_client)

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins.collection_mixin import AsyncCollectionMixin, CollectionMixin
from mpt_api_client.http.mixins.create_file_mixin import AsyncCreateFileMixin, CreateFileMixin
from mpt_api_client.http.mixins.delete_mixin import AsyncDeleteMixin, DeleteMixin
from mpt_api_client.http.mixins.get_mixin import AsyncGetMixin, GetMixin
from mpt_api_client.http.mixins.update_file_mixin import AsyncUpdateFileMixin, UpdateFileMixin
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel, ResourceData
from mpt_api_client.resources.mixins import (
    AsyncPublishableMixin,
    PublishableMixin,
)
from mpt_api_client.resources.program.programs_documents import (
    AsyncDocumentService,
    DocumentService,
)
from mpt_api_client.resources.program.programs_media import (
    AsyncMediaService,
    MediaService,
)
from mpt_api_client.resources.program.programs_parameter_groups import (
    AsyncParameterGroupsService,
    ParameterGroupsService,
)
from mpt_api_client.resources.program.programs_parameters import (
    AsyncParametersService,
    ParametersService,
)
from mpt_api_client.resources.program.programs_templates import (
    AsyncTemplatesService,
    TemplatesService,
)
from mpt_api_client.resources.program.programs_terms import (
    AsyncTermService,
    TermService,
)


class Program(Model):
    """Program resource.

    Attributes:
        name: Program name.
        website: Program website.
        eligibility: Eligibility criteria for the program.
        applicable_to: Applicable products or services for the program.
        icon: Program icon URL.
        status: Program status.
        vendor: Reference to the vendor account associated with the program.
        settings: Program settings.
        statistics: Program statistics and performance metrics.
        audit: Audit information related to the program (created, updated events).
    """

    name: str | None
    website: str | None
    eligibility: BaseModel | None
    applicable_to: str | None
    icon: str | None
    status: str | None
    vendor: BaseModel | None
    settings: BaseModel | None
    statistics: BaseModel | None
    audit: BaseModel | None


class ProgramsServiceConfig:
    """Programs service configuration."""

    _endpoint = "/public/v1/program/programs"
    _model_class = Program
    _collection_key = "data"
    _upload_file_key = "icon"
    _upload_data_key = "program"


class ProgramsService(
    GetMixin[Program],
    CreateFileMixin[Program],
    UpdateFileMixin[Program],
    DeleteMixin,
    PublishableMixin[Program],
    CollectionMixin[Program],
    Service[Program],
    ProgramsServiceConfig,
):
    """Programs service."""

    def update_settings(self, program_id: str, settings: ResourceData) -> Program:
        """Update program settings.

        Args:
            program_id: Program ID
            settings: Settings data to be updated
        """
        return self._resource(program_id).put("settings", json=settings)

    def documents(self, program_id: str) -> DocumentService:
        """Return program documents service."""
        return DocumentService(
            http_client=self.http_client, endpoint_params={"program_id": program_id}
        )

    def media(self, program_id: str) -> MediaService:
        """Return program media service."""
        return MediaService(
            http_client=self.http_client, endpoint_params={"program_id": program_id}
        )

    def parameter_groups(self, program_id: str) -> ParameterGroupsService:
        """Return program parameter groups service."""
        return ParameterGroupsService(
            http_client=self.http_client, endpoint_params={"program_id": program_id}
        )

    def parameters(self, program_id: str) -> ParametersService:  # noqa: WPS110
        """Return program parameters service."""
        return ParametersService(
            http_client=self.http_client, endpoint_params={"program_id": program_id}
        )

    def templates(self, program_id: str) -> TemplatesService:
        """Return program templates service."""
        return TemplatesService(
            http_client=self.http_client, endpoint_params={"program_id": program_id}
        )

    def terms(self, program_id: str) -> TermService:
        """Return program terms service."""
        return TermService(http_client=self.http_client, endpoint_params={"program_id": program_id})


class AsyncProgramsService(
    AsyncGetMixin[Program],
    AsyncCreateFileMixin[Program],
    AsyncUpdateFileMixin[Program],
    AsyncDeleteMixin,
    AsyncPublishableMixin[Program],
    AsyncCollectionMixin[Program],
    AsyncService[Program],
    ProgramsServiceConfig,
):
    """Async programs service."""

    async def update_settings(self, program_id: str, settings: ResourceData) -> Program:
        """Update program settings.

        Args:
            program_id: Program ID
            settings: Settings data to be updated
        """
        return await self._resource(program_id).put("settings", json=settings)

    def documents(self, program_id: str) -> AsyncDocumentService:
        """Return async program documents service."""
        return AsyncDocumentService(
            http_client=self.http_client, endpoint_params={"program_id": program_id}
        )

    def media(self, program_id: str) -> AsyncMediaService:
        """Return async program media service."""
        return AsyncMediaService(
            http_client=self.http_client, endpoint_params={"program_id": program_id}
        )

    def parameter_groups(self, program_id: str) -> AsyncParameterGroupsService:
        """Return async program parameter groups service."""
        return AsyncParameterGroupsService(
            http_client=self.http_client, endpoint_params={"program_id": program_id}
        )

    def parameters(self, program_id: str) -> AsyncParametersService:  # noqa: WPS110
        """Return async program parameters service."""
        return AsyncParametersService(
            http_client=self.http_client, endpoint_params={"program_id": program_id}
        )

    def templates(self, program_id: str) -> AsyncTemplatesService:
        """Return async program templates service."""
        return AsyncTemplatesService(
            http_client=self.http_client, endpoint_params={"program_id": program_id}
        )

    def terms(self, program_id: str) -> AsyncTermService:
        """Return async program terms service."""
        return AsyncTermService(
            http_client=self.http_client, endpoint_params={"program_id": program_id}
        )

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncDisableMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    DisableMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model, ResourceData
from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.notifications.template_variants import (
    AsyncTemplateVariantsService,
    TemplateVariantsService,
)


class Template(Model):
    """Notifications Template resource.

    Attributes:
        name: Template name.
        category: Reference to the notification category of the template.
        criteria: Criteria triggering the template automatically.
        default_variant: Reference to the default variant of the template.
        description: Template description.
        last_used: Timestamp of the last time the template was used.
        owner: Reference to the account owning the template.
        schedule: Reference to the schedule triggering the template.
        statistics: Usage statistics of the template.
        status: Template status.
        type: How the template is triggered (Event, Scheduled or Manual).
        variants: References to the language-specific variants of the template.
        external_id: External identifier of the template.
        audit: Audit information (created, updated events).
    """

    name: str | None
    category: BaseModel | None
    criteria: BaseModel | None
    default_variant: BaseModel | None
    description: str | None
    last_used: str | None
    owner: BaseModel | None
    schedule: BaseModel | None
    statistics: BaseModel | None
    status: str | None
    type: str | None
    variants: list[BaseModel] | None
    external_id: str | None
    audit: BaseModel | None


class TemplatesServiceConfig:
    """Notifications Templates service configuration."""

    _endpoint = "/public/v1/notifications/templates"
    _model_class = Template
    _collection_key = "data"


class TemplatesService(
    DisableMixin[Template],
    ManagedResourceMixin[Template],
    CollectionMixin[Template],
    Service[Template],
    TemplatesServiceConfig,
):
    """Notifications Templates service."""

    def activate(self, resource_id: str, resource_data: ResourceData | None = None) -> Template:
        """Switch template to active state."""
        return self._resource(resource_id).post("activate", json=resource_data)

    def variants(self, template_id: str) -> TemplateVariantsService:
        """Access template variants service.

        Args:
            template_id: Template ID.

        Returns:
            TemplateVariantsService
        """
        return TemplateVariantsService(
            http_client=self.http_client,
            endpoint_params={"template_id": template_id},
        )


class AsyncTemplatesService(
    AsyncDisableMixin[Template],
    AsyncManagedResourceMixin[Template],
    AsyncCollectionMixin[Template],
    AsyncService[Template],
    TemplatesServiceConfig,
):
    """Async Notifications Templates service."""

    async def activate(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> Template:
        """Switch template to active state."""
        return await self._resource(resource_id).post("activate", json=resource_data)

    def variants(self, template_id: str) -> AsyncTemplateVariantsService:
        """Access async template variants service.

        Args:
            template_id: Template ID.

        Returns:
            AsyncTemplateVariantsService
        """
        return AsyncTemplateVariantsService(
            http_client=self.http_client,
            endpoint_params={"template_id": template_id},
        )

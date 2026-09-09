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


class TemplateVariant(Model):
    """Notifications Template Variant resource.

    Attributes:
        body: Body content of the variant.
        default: Whether this variant is the default one of its template.
        language_code: Language code of the variant.
        template: Reference to the parent template.
        status: Variant status.
        subject: Subject of the messages created from this variant.
        audit: Audit information (created, updated events).
    """

    body: str | None
    default: bool | None
    language_code: str | None
    template: BaseModel | None
    status: str | None
    subject: str | None
    audit: BaseModel | None


class TemplateVariantsServiceConfig:
    """Notifications Template Variants service configuration."""

    _endpoint = "/public/v1/notifications/templates/{template_id}/variants"
    _model_class = TemplateVariant
    _collection_key = "data"


class TemplateVariantsService(
    DisableMixin[TemplateVariant],
    ManagedResourceMixin[TemplateVariant],
    CollectionMixin[TemplateVariant],
    Service[TemplateVariant],
    TemplateVariantsServiceConfig,
):
    """Notifications Template Variants service."""

    def activate(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> TemplateVariant:
        """Switch template variant to active state."""
        return self._resource(resource_id).post("activate", json=resource_data)


class AsyncTemplateVariantsService(
    AsyncDisableMixin[TemplateVariant],
    AsyncManagedResourceMixin[TemplateVariant],
    AsyncCollectionMixin[TemplateVariant],
    AsyncService[TemplateVariant],
    TemplateVariantsServiceConfig,
):
    """Async Notifications Template Variants service."""

    async def activate(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> TemplateVariant:
        """Switch template variant to active state."""
        return await self._resource(resource_id).post("activate", json=resource_data)

from mpt_api_client.models import Model as BaseModel
from mpt_api_client.models import ResourceData


class AsyncDisableMixin[Model: BaseModel]:
    """Disable resource mixin."""

    async def disable(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Disable a specific resource."""
        return await self._resource(resource_id).post("disable", json=resource_data)  # type: ignore[attr-defined, no-any-return]


class DisableMixin[Model: BaseModel]:
    """Disable resource mixin."""

    def disable(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Disable a specific resource."""
        return self._resource(resource_id).post("disable", json=resource_data)  # type: ignore[attr-defined, no-any-return]

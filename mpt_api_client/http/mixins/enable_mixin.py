from mpt_api_client.models import Model as BaseModel
from mpt_api_client.models import ResourceData


class AsyncEnableMixin[Model: BaseModel]:
    """Enable resource mixin."""

    async def enable(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Enable a specific resource."""
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id=resource_id, method="POST", action="enable", json=resource_data
        )


class EnableMixin[Model: BaseModel]:
    """Enable resource mixin."""

    def enable(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Enable a specific resource."""
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id=resource_id, method="POST", action="enable", json=resource_data
        )

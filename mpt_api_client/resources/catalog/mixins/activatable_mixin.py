from mpt_api_client.models import ResourceData


class ActivatableMixin[Model]:
    """Activatable mixin adds the ability to activate and deactivate."""

    def activate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Active."""
        return self._resource(resource_id).post("activate", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    def deactivate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Inactive."""
        return self._resource(resource_id).post("deactivate", json=resource_data)  # type: ignore[attr-defined, no-any-return]


class AsyncActivatableMixin[Model]:
    """Activatable mixin adds the ability to activate and deactivate."""

    async def activate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Active."""
        return await self._resource(resource_id).post("activate", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    async def deactivate(
        self,
        resource_id: str,
        resource_data: ResourceData | None = None,
    ) -> Model:
        """Update state to Inactive."""
        return await self._resource(resource_id).post("deactivate", json=resource_data)  # type: ignore[attr-defined, no-any-return]

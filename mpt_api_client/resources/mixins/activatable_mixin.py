from mpt_api_client.models import ResourceData


class ActivatableMixin[Model]:
    """Activatable mixin for activating and deactivating resources."""

    def activate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Activate a resource."""
        return self._resource(resource_id).post("activate", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    def deactivate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Deactivate a resource."""
        return self._resource(resource_id).post("deactivate", json=resource_data)  # type: ignore[attr-defined, no-any-return]


class AsyncActivatableMixin[Model]:
    """Async activatable mixin for activating and deactivating resources."""

    async def activate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Activate a resource."""
        return await self._resource(resource_id).post("activate", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    async def deactivate(
        self,
        resource_id: str,
        resource_data: ResourceData | None = None,
    ) -> Model:
        """Deactivate a resource."""
        return await self._resource(resource_id).post("deactivate", json=resource_data)  # type: ignore[attr-defined, no-any-return]

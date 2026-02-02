from mpt_api_client.models import ResourceData


class ActivatableMixin[Model]:
    """Activatable mixin adds the ability to activate and deactivate."""

    def activate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Active.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "activate", json=resource_data
        )

    def deactivate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Inactive.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "deactivate", json=resource_data
        )


class AsyncActivatableMixin[Model]:
    """Activatable mixin adds the ability to activate and deactivate."""

    async def activate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Active.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "activate", json=resource_data
        )

    async def deactivate(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> Model:
        """Update state to Inactive.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "deactivate", json=resource_data
        )

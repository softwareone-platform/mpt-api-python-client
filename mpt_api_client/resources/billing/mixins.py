from mpt_api_client.models import ResourceData


# TODO: Consider moving Regeneratable mixins to http/mixins if publishable and activatable are moved
class RegeneratableMixin[Model]:
    """Regeneratable mixin adds the ability to regenerate resources."""

    def regenerate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Regenerate resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "regenerate", json=resource_data
        )

    def submit(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Submit resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "submit", json=resource_data
        )

    def enquiry(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Enquiry resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "enquiry", json=resource_data
        )

    def accept(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Accept resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "accept", json=resource_data
        )


class AsyncRegeneratableMixin[Model]:
    """Regeneratable mixin adds the ability to regenerate resources."""

    async def regenerate(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> Model:
        """Regenerate resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "regenerate", json=resource_data
        )

    async def submit(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Submit resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "submit", json=resource_data
        )

    async def enquiry(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Enquiry resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "enquiry", json=resource_data
        )

    async def accept(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Accept resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "accept", json=resource_data
        )

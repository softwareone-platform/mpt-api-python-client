from mpt_api_client.models import ResourceData


class RegeneratableMixin[Model]:
    """Regeneratable mixin adds the ability to regenerate resources."""

    def regenerate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Regenerate resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource(resource_id).post("regenerate", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    def submit(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Submit resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource(resource_id).post("submit", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    def enquiry(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Enquiry resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource(resource_id).post("enquiry", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    def accept(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Accept resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource(resource_id).post("accept", json=resource_data)  # type: ignore[attr-defined, no-any-return]


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
        return await self._resource(resource_id).post("regenerate", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    async def submit(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Submit resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource(resource_id).post("submit", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    async def enquiry(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Enquiry resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource(resource_id).post("enquiry", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    async def accept(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Accept resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource(resource_id).post("accept", json=resource_data)  # type: ignore[attr-defined, no-any-return]

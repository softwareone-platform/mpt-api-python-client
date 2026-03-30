from mpt_api_client.models import ResourceData


class IssuableMixin[Model]:
    """Issuable mixin adds the ability to issue resources."""

    def issue(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Issue resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource(resource_id).post("issue", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    def cancel(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Cancel resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource(resource_id).post("cancel", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    def error(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Error resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource(resource_id).post("error", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    def pending(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Pending resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource(resource_id).post("pending", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    def queue(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Queue resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource(resource_id).post("queue", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    def retry(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Retry resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource(resource_id).post("retry", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    def recalculate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Recalculate resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource(resource_id).post("recalculate", json=resource_data)  # type: ignore[attr-defined, no-any-return]


class AsyncIssuableMixin[Model]:
    """Issuable mixin adds the ability to issue resources."""

    async def issue(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Issue resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource(resource_id).post("issue", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    async def cancel(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Cancel resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource(resource_id).post("cancel", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    async def error(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Error resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource(resource_id).post("error", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    async def pending(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Pending resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource(resource_id).post("pending", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    async def queue(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Queue resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource(resource_id).post("queue", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    async def retry(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Retry resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource(resource_id).post("retry", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    async def recalculate(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> Model:
        """Recalculate resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource(resource_id).post("recalculate", json=resource_data)  # type: ignore[attr-defined, no-any-return]

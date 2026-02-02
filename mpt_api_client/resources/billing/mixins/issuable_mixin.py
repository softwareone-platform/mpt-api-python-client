from mpt_api_client.models import ResourceData


class IssuableMixin[Model]:
    """Issuable mixin adds the ability to issue resources."""

    def issue(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Issue resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "issue", json=resource_data
        )

    def cancel(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Cancel resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "cancel", json=resource_data
        )

    def error(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Error resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "error", json=resource_data
        )

    def pending(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Pending resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "pending", json=resource_data
        )

    def queue(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Queue resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "queue", json=resource_data
        )

    def retry(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Retry resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "retry", json=resource_data
        )

    def recalculate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Recalculate resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "recalculate", json=resource_data
        )


class AsyncIssuableMixin[Model]:
    """Issuable mixin adds the ability to issue resources."""

    async def issue(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Issue resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "issue", json=resource_data
        )

    async def cancel(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Cancel resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "cancel", json=resource_data
        )

    async def error(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Error resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "error", json=resource_data
        )

    async def pending(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Pending resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "pending", json=resource_data
        )

    async def queue(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Queue resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "queue", json=resource_data
        )

    async def retry(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Retry resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "retry", json=resource_data
        )

    async def recalculate(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> Model:
        """Recalculate resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "recalculate", json=resource_data
        )

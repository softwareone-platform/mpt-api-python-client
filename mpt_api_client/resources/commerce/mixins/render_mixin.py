class RenderMixin[Model]:
    """Render resource mixin."""

    def render(self, resource_id: str) -> str:
        """Render resource.

        Args:
            resource_id: Resource ID

        Returns:
            Rendered resource.
        """
        response = self._resource_do_request(resource_id, action="render")  # type: ignore[attr-defined]
        return response.text  # type: ignore[no-any-return]


class AsyncRenderMixin[Model]:
    """Asynchronous render resource mixin."""

    async def render(self, resource_id: str) -> str:
        """Render resource.

        Args:
            resource_id: Resource ID

        Returns:
            Rendered resource.
        """
        response = await self._resource_do_request(resource_id, action="render")  # type: ignore[attr-defined]
        return response.text  # type: ignore[no-any-return]

from mpt_api_client.models.model import ResourceData


class TerminateMixin[Model]:
    """Terminate resource mixin."""

    def terminate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Terminate resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data

        Returns:
            Terminated resource.
        """
        return self._resource_action(resource_id, "POST", "terminate", json=resource_data)  # type: ignore[attr-defined, no-any-return]


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


class TemplateMixin[Model]:
    """Template resource mixin."""

    def template(self, resource_id: str) -> str:
        """Get resource template.

        Args:
            resource_id: Resource ID

        Returns:
            Resource template.
        """
        response = self._resource_do_request(resource_id, action="template")  # type: ignore[attr-defined]
        return response.text  # type: ignore[no-any-return]


class AsyncTerminateMixin[Model]:
    """Asynchronous terminate resource mixin."""

    async def terminate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Terminate resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data

        Returns:
            Terminated resource.
        """
        return await self._resource_action(resource_id, "POST", "terminate", json=resource_data)  # type: ignore[attr-defined, no-any-return]


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


class AsyncTemplateMixin[Model]:
    """Asynchronous template resource mixin."""

    async def template(self, resource_id: str) -> str:
        """Get resource template.

        Args:
            resource_id: Resource ID

        Returns:
            Resource template.
        """
        response = await self._resource_do_request(resource_id, action="template")  # type: ignore[attr-defined]
        return response.text  # type: ignore[no-any-return]

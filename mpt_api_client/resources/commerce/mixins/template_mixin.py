class TemplateMixin[Model]:
    """Template resource mixin."""

    def template(self, resource_id: str) -> str:
        """Get resource template.

        Args:
            resource_id: Resource ID

        Returns:
            Resource template.
        """
        response = self._resource(resource_id).do_request("GET", "template")  # type: ignore[attr-defined]
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
        response = await self._resource(resource_id).do_request("GET", "template")  # type: ignore[attr-defined]
        return response.text  # type: ignore[no-any-return]

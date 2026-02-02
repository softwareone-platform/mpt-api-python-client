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


class AsyncTemplateMixin[Model]:
    """Asynchronous template resource mixin."""

    async def template(self, resource_id: str) -> str:
        """Get resource template.

        Args:
            resource_id: Resource ID

        Returns:
            Resource template.
        """
        # pylint: disable=duplicate-code
        response = await self._resource_do_request(resource_id, action="template")  # type: ignore[attr-defined]
        return response.text  # type: ignore[no-any-return]

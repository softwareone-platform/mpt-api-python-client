from mpt_api_client.models import ResourceData


class ValidateMixin[Model]:
    """Validate mixin adds the ability to validate a resource."""

    def validate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Validate a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be validated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "validate", json=resource_data
        )


class AsyncValidateMixin[Model]:
    """Asynchronous Validate mixin adds the ability to validate a resource."""

    async def validate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Validate a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be validated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "validate", json=resource_data
        )

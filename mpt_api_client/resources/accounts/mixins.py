from mpt_api_client.models import ResourceData

# TODO: Consider reorganizing functions in mixins to reduce duplication and differences amongst
#       different domains


class ActivatableMixin[Model]:
    """Activatable mixin for activating, enabling, disabling and deactivating resources."""

    def activate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Activate a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "activate", json=resource_data
        )

    def deactivate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Deactivate a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "deactivate", json=resource_data
        )


class EnablableMixin[Model]:
    """Enablable mixin for enabling and disabling resources."""

    def enable(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Enable a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "enable", json=resource_data
        )

    def disable(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Disable a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "disable", json=resource_data
        )


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


class AsyncActivatableMixin[Model]:
    """Async activatable mixin for activating, enabling, disabling and deactivating resources."""

    async def activate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Activate a resource.

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
        """Deactivate a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "deactivate", json=resource_data
        )


class AsyncEnablableMixin[Model]:
    """Asynchronous Enablable mixin for enabling and disabling resources."""

    async def enable(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Enable a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "enable", json=resource_data
        )

    async def disable(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Disable a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "disable", json=resource_data
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

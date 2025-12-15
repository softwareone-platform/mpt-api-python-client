from mpt_api_client.models import ResourceData


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


class BlockableMixin[Model]:
    """Blockable mixin for blocking and unblocking resources."""

    def block(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Block a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "block", json=resource_data
        )

    def unblock(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Unblock a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "unblock", json=resource_data
        )


class InvitableMixin[Model]:
    """Invitable mixin for sending and managing invites for resources."""

    def accept_invite(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Accept an invite for a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "accept-invite", json=resource_data
        )

    def resend_invite(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Resend an invite to a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "resend-invite", json=resource_data
        )

    def send_new_invite(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Send a new invite to a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "send-new-invite", json=resource_data
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


class AsyncBlockableMixin[Model]:
    """Asynchronous Blockable mixin for blocking and unblocking resources."""

    async def block(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Block a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "block", json=resource_data
        )

    async def unblock(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Unblock a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "unblock", json=resource_data
        )


class AsyncInvitableMixin[Model]:
    """Asynchronous Invitable mixin for sending and managing invites for resources."""

    async def accept_invite(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> Model:
        """Accept an invite for a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "accept-invite", json=resource_data
        )

    async def resend_invite(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> Model:
        """Resend an invite to a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "resend-invite", json=resource_data
        )

    async def send_new_invite(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> Model:
        """Send a new invite to a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "send-new-invite", json=resource_data
        )

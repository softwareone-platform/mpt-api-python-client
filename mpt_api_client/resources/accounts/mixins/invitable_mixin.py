from mpt_api_client.models import ResourceData


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

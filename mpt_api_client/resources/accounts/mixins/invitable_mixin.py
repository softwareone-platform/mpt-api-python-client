from mpt_api_client.models import ResourceData


class InvitableMixin[Model]:
    """Invitable mixin for sending and managing invites for resources."""

    def accept_invite(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Accept an invite for a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource(resource_id).post("accept-invite", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    def resend_invite(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Resend an invite to a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource(resource_id).post("resend-invite", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    def send_new_invite(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Send a new invite to a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource(resource_id).post("send-new-invite", json=resource_data)  # type: ignore[attr-defined, no-any-return]


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
        return await self._resource(resource_id).post("accept-invite", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    async def resend_invite(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> Model:
        """Resend an invite to a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource(resource_id).post("resend-invite", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    async def send_new_invite(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> Model:
        """Send a new invite to a resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource(resource_id).post("send-new-invite", json=resource_data)  # type: ignore[attr-defined, no-any-return]

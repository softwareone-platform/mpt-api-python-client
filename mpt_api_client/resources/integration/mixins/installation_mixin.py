from mpt_api_client.models import ResourceData


class InstallationMixin[Model]:
    """Mixin that adds installation lifecycle actions: invite, install, uninstall, expire."""

    def invite(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Invite an installation.

        Args:
            resource_id: Installation ID.
            resource_data: Optional request body.

        Returns:
            Updated installation.
        """
        return self._resource(resource_id).post("invite", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    def install(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Mark an installation as installed.

        Args:
            resource_id: Installation ID.
            resource_data: Optional request body.

        Returns:
            Updated installation.
        """
        return self._resource(resource_id).post("install", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    def uninstall(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Uninstall an installation.

        Args:
            resource_id: Installation ID.
            resource_data: Optional request body.

        Returns:
            Updated installation.
        """
        return self._resource(resource_id).post("uninstall", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    def expire(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Expire an installation.

        Args:
            resource_id: Installation ID.
            resource_data: Optional request body.

        Returns:
            Updated installation.
        """
        return self._resource(resource_id).post("expire", json=resource_data)  # type: ignore[attr-defined, no-any-return]


class AsyncInstallationMixin[Model]:
    """Async mixin for installation lifecycle actions: invite, install, uninstall, expire."""

    async def invite(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Invite an installation.

        Args:
            resource_id: Installation ID.
            resource_data: Optional request body.

        Returns:
            Updated installation.
        """
        return await self._resource(resource_id).post("invite", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    async def install(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Mark an installation as installed.

        Args:
            resource_id: Installation ID.
            resource_data: Optional request body.

        Returns:
            Updated installation.
        """
        return await self._resource(resource_id).post("install", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    async def uninstall(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Uninstall an installation.

        Args:
            resource_id: Installation ID.
            resource_data: Optional request body.

        Returns:
            Updated installation.
        """
        return await self._resource(resource_id).post("uninstall", json=resource_data)  # type: ignore[attr-defined, no-any-return]

    async def expire(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Expire an installation.

        Args:
            resource_id: Installation ID.
            resource_data: Optional request body.

        Returns:
            Updated installation.
        """
        return await self._resource(resource_id).post("expire", json=resource_data)  # type: ignore[attr-defined, no-any-return]

from mpt_api_client.models import ResourceData


class InstallationMixin[Model]:
    """Mixin that adds the installation redeem action."""

    def redeem(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Redeem an installation invitation.

        Args:
            resource_id: Installation ID.
            resource_data: Redeem payload, for example ``{"code": "...", "modules": [...]}``.

        Returns:
            Updated installation.
        """
        return self._resource(resource_id).post("redeem", json=resource_data)  # type: ignore[attr-defined, no-any-return]


class AsyncInstallationMixin[Model]:
    """Async mixin that adds the installation redeem action."""

    async def redeem(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Redeem an installation invitation.

        Args:
            resource_id: Installation ID.
            resource_data: Redeem payload, for example ``{"code": "...", "modules": [...]}``.

        Returns:
            Updated installation.
        """
        return await self._resource(resource_id).post("redeem", json=resource_data)  # type: ignore[attr-defined, no-any-return]

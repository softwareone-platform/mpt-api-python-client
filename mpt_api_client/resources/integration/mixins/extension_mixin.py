from mpt_api_client.models import FileModel


class ExtensionMixin[Model]:
    """Mixin that adds extension-specific actions: publish, unpublish, regenerate, token, icon."""

    def publish(self, resource_id: str) -> Model:
        """Publish the extension, moving it to Public status.

        Args:
            resource_id: Extension ID.

        Returns:
            Updated extension.
        """
        return self._resource(resource_id).post("publish")  # type: ignore[attr-defined, no-any-return]

    def unpublish(self, resource_id: str) -> Model:
        """Unpublish the extension, moving it to Private status.

        Args:
            resource_id: Extension ID.

        Returns:
            Updated extension.
        """
        return self._resource(resource_id).post("unpublish")  # type: ignore[attr-defined, no-any-return]

    def regenerate(self, resource_id: str) -> Model:
        """Regenerate the extension credentials.

        Args:
            resource_id: Extension ID.

        Returns:
            Updated extension.
        """
        return self._resource(resource_id).post("regenerate")  # type: ignore[attr-defined, no-any-return]

    def token(self, resource_id: str) -> Model:
        """Retrieve an access token for the extension.

        Args:
            resource_id: Extension ID.

        Returns:
            Token response.
        """
        return self._resource(resource_id).post("token")  # type: ignore[attr-defined, no-any-return]

    def download_icon(self, resource_id: str) -> FileModel:
        """Download the icon for the given extension.

        Args:
            resource_id: Extension ID.

        Returns:
            File model containing the downloaded icon.
        """
        response = self._resource(resource_id).do_request("GET", "icon")  # type: ignore[attr-defined]
        return FileModel(response)


class AsyncExtensionMixin[Model]:
    """Async mixin for extension-specific actions: publish, unpublish, regenerate, token, icon."""

    async def publish(self, resource_id: str) -> Model:
        """Publish the extension, moving it to Public status.

        Args:
            resource_id: Extension ID.

        Returns:
            Updated extension.
        """
        return await self._resource(resource_id).post("publish")  # type: ignore[attr-defined, no-any-return]

    async def unpublish(self, resource_id: str) -> Model:
        """Unpublish the extension, moving it to Private status.

        Args:
            resource_id: Extension ID.

        Returns:
            Updated extension.
        """
        return await self._resource(resource_id).post("unpublish")  # type: ignore[attr-defined, no-any-return]

    async def regenerate(self, resource_id: str) -> Model:
        """Regenerate the extension credentials.

        Args:
            resource_id: Extension ID.

        Returns:
            Updated extension.
        """
        return await self._resource(resource_id).post("regenerate")  # type: ignore[attr-defined, no-any-return]

    async def token(self, resource_id: str) -> Model:
        """Retrieve an access token for the extension.

        Args:
            resource_id: Extension ID.

        Returns:
            Token response.
        """
        return await self._resource(resource_id).post("token")  # type: ignore[attr-defined, no-any-return]

    async def download_icon(self, resource_id: str) -> FileModel:
        """Download the icon for the given extension.

        Args:
            resource_id: Extension ID.

        Returns:
            File model containing the downloaded icon.
        """
        response = await self._resource(resource_id).do_request("GET", "icon")  # type: ignore[attr-defined]
        return FileModel(response)

from mpt_api_client.models import ResourceData


class CreateMixin[Model]:
    """Create resource mixin."""

    def create(self, resource_data: ResourceData) -> Model:
        """Create a new resource using `POST /endpoint`.

        Returns:
            New resource created.
        """
        response = self.http_client.request("post", self.path, json=resource_data)  # type: ignore[attr-defined]

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]


class AsyncCreateMixin[Model]:
    """Create resource mixin."""

    async def create(self, resource_data: ResourceData) -> Model:
        """Create a new resource using `POST /endpoint`.

        Returns:
            New resource created.
        """
        response = await self.http_client.request("post", self.path, json=resource_data)  # type: ignore[attr-defined]

        return self._model_class.from_response(response)  # type: ignore[attr-defined, no-any-return]

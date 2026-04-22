from mpt_api_client.models import ResourceData


class ReviewableMixin[Model]:
    """Reviewable mixin adds the ability to review a resource."""

    def review(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Review the resource."""
        return self._resource(resource_id).post("review", json=resource_data)  # type: ignore[attr-defined, no-any-return]


class AsyncReviewableMixin[Model]:
    """Async reviewable mixin adds the ability to review a resource."""

    async def review(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Review the resource."""
        return await self._resource(resource_id).post("review", json=resource_data)  # type: ignore[attr-defined, no-any-return]

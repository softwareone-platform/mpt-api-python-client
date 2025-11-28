from mpt_api_client.http.mixins import (
    AsyncCreateFileMixin,
    AsyncDownloadFileMixin,
    CreateFileMixin,
    DownloadFileMixin,
)
from mpt_api_client.models import ResourceData


# TODO: Consider moving publishable and activatable mixins to http/mixins
class PublishableMixin[Model]:
    """Publishable mixin adds the ability to review, publish and unpublish."""

    def review(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Pending.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "review", json=resource_data
        )

    def publish(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Published.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "publish", json=resource_data
        )

    def unpublish(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Unpublished.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "unpublish", json=resource_data
        )


class AsyncPublishableMixin[Model]:
    """Publishable mixin adds the ability to review, publish and unpublish."""

    async def review(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to reviewing.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "review", json=resource_data
        )

    async def publish(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Published.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "publish", json=resource_data
        )

    async def unpublish(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Unpublished.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "unpublish", json=resource_data
        )


class AsyncDocumentMixin[Model](
    AsyncCreateFileMixin[Model],
    AsyncDownloadFileMixin[Model],
    AsyncPublishableMixin[Model],
):
    """Async document mixin."""


class DocumentMixin[Model](
    CreateFileMixin[Model],
    DownloadFileMixin[Model],
    PublishableMixin[Model],
):
    """Document mixin."""


class MediaMixin[Model](
    CreateFileMixin[Model],
    DownloadFileMixin[Model],
    PublishableMixin[Model],
):
    """Media mixin."""


class ActivatableMixin[Model]:
    """Activatable mixin adds the ability to activate and deactivate."""

    def activate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Active.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "activate", json=resource_data
        )

    def deactivate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Inactive.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "deactivate", json=resource_data
        )


class AsyncActivatableMixin[Model]:
    """Activatable mixin adds the ability to activate and deactivate."""

    async def activate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Update state to Active.

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
        """Update state to Inactive.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "deactivate", json=resource_data
        )


class AsyncMediaMixin[Model](
    AsyncCreateFileMixin[Model],
    AsyncDownloadFileMixin[Model],
    AsyncPublishableMixin[Model],
):
    """Media mixin."""

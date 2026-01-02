from mpt_api_client.http.mixins import (
    AsyncCreateFileMixin,
    AsyncDeleteMixin,
    AsyncDownloadFileMixin,
    AsyncGetMixin,
    AsyncUpdateMixin,
    CreateFileMixin,
    DeleteMixin,
    DownloadFileMixin,
    GetMixin,
    UpdateMixin,
)
from mpt_api_client.models import ResourceData


# TODO: Consider moving Regeneratable mixins to http/mixins if publishable and activatable are moved
# TODO: Consider reorganizing functions in mixins to reduce duplication and differences amongst
#       different domains
class RegeneratableMixin[Model]:
    """Regeneratable mixin adds the ability to regenerate resources."""

    def regenerate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Regenerate resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "regenerate", json=resource_data
        )

    def submit(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Submit resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "submit", json=resource_data
        )

    def enquiry(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Enquiry resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "enquiry", json=resource_data
        )

    def accept(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Accept resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "accept", json=resource_data
        )


class AsyncRegeneratableMixin[Model]:
    """Regeneratable mixin adds the ability to regenerate resources."""

    async def regenerate(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> Model:
        """Regenerate resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "regenerate", json=resource_data
        )

    async def submit(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Submit resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "submit", json=resource_data
        )

    async def enquiry(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Enquiry resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "enquiry", json=resource_data
        )

    async def accept(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Accept resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "accept", json=resource_data
        )


class RecalculatableMixin[Model]:
    """Recalculatable mixin adds the ability to recalculate resources."""

    def recalculate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Recalculate resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "recalculate", json=resource_data
        )

    def accept(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Accept resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "accept", json=resource_data
        )

    def queue(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Queue resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "queue", json=resource_data
        )


class AsyncRecalculatableMixin[Model]:
    """Recalculatable mixin adds the ability to recalculate resources."""

    async def recalculate(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> Model:
        """Recalculate resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "recalculate", json=resource_data
        )

    async def accept(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Accept resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "accept", json=resource_data
        )

    async def queue(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Queue resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "queue", json=resource_data
        )


class IssuableMixin[Model]:
    """Issuable mixin adds the ability to issue resources."""

    def issue(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Issue resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "issue", json=resource_data
        )

    def cancel(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Cancel resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "cancel", json=resource_data
        )

    def error(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Error resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "error", json=resource_data
        )

    def pending(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Pending resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "pending", json=resource_data
        )

    def queue(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Queue resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "queue", json=resource_data
        )

    def retry(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Retry resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "retry", json=resource_data
        )

    def recalculate(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Recalculate resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "recalculate", json=resource_data
        )


class AsyncIssuableMixin[Model]:
    """Issuable mixin adds the ability to issue resources."""

    async def issue(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Issue resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "issue", json=resource_data
        )

    async def cancel(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Cancel resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "cancel", json=resource_data
        )

    async def error(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Error resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "error", json=resource_data
        )

    async def pending(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Pending resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "pending", json=resource_data
        )

    async def queue(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Queue resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "queue", json=resource_data
        )

    async def retry(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Retry resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "retry", json=resource_data
        )

    async def recalculate(
        self, resource_id: str, resource_data: ResourceData | None = None
    ) -> Model:
        """Recalculate resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "recalculate", json=resource_data
        )


class AcceptableMixin[Model]:
    """Acceptable mixin adds the ability to accept resources."""

    def accept(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Accept resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "accept", json=resource_data
        )

    def queue(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Queue resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "queue", json=resource_data
        )


class AsyncAcceptableMixin[Model]:
    """Acceptable mixin adds the ability to accept resources."""

    async def accept(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Accept resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "accept", json=resource_data
        )

    async def queue(self, resource_id: str, resource_data: ResourceData | None = None) -> Model:
        """Queue resource.

        Args:
            resource_id: Resource ID
            resource_data: Resource data will be updated
        """
        return await self._resource_action(  # type: ignore[attr-defined, no-any-return]
            resource_id, "POST", "queue", json=resource_data
        )


class AttachmentMixin[Model](
    CreateFileMixin[Model],
    UpdateMixin[Model],
    DeleteMixin,
    DownloadFileMixin[Model],
    GetMixin[Model],
):
    """Attachment mixin."""


class AsyncAttachmentMixin[Model](
    AsyncCreateFileMixin[Model],
    AsyncUpdateMixin[Model],
    AsyncDeleteMixin,
    AsyncDownloadFileMixin[Model],
    AsyncGetMixin[Model],
):
    """Async Attachment mixin."""

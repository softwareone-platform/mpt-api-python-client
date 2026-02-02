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

from mpt_api_client.http import mixins


class AttachmentMixin[Model](
    mixins.CreateFileMixin[Model],
    mixins.UpdateMixin[Model],
    mixins.DeleteMixin,
    mixins.DownloadFileMixin[Model],
    mixins.GetMixin[Model],
):
    """Attachment mixin."""


class AsyncAttachmentMixin[Model](
    mixins.AsyncCreateFileMixin[Model],
    mixins.AsyncUpdateMixin[Model],
    mixins.AsyncDeleteMixin,
    mixins.AsyncDownloadFileMixin[Model],
    mixins.AsyncGetMixin[Model],
):
    """Async Attachment mixin."""

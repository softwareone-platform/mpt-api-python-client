from mpt_api_client.http.mixins import (
    AsyncCreateFileMixin,
    AsyncDownloadFileMixin,
    CreateFileMixin,
    DownloadFileMixin,
)
from mpt_api_client.resources.mixins.publishable_mixin import (
    AsyncPublishableMixin,
    PublishableMixin,
)


class DocumentMixin[Model](
    CreateFileMixin[Model],
    DownloadFileMixin[Model],
    PublishableMixin[Model],
):
    """Document mixin."""


class AsyncDocumentMixin[Model](
    AsyncCreateFileMixin[Model],
    AsyncDownloadFileMixin[Model],
    AsyncPublishableMixin[Model],
):
    """Async document mixin."""

from mpt_api_client.http.mixins import (
    AsyncCreateFileMixin,
    AsyncDownloadFileMixin,
    CreateFileMixin,
    DownloadFileMixin,
)
from mpt_api_client.resources.catalog.mixins.publishable_mixin import (
    AsyncPublishableMixin,
    PublishableMixin,
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

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


class MediaMixin[Model](
    CreateFileMixin[Model],
    DownloadFileMixin[Model],
    PublishableMixin[Model],
):
    """Media mixin."""


class AsyncMediaMixin[Model](
    AsyncCreateFileMixin[Model],
    AsyncDownloadFileMixin[Model],
    AsyncPublishableMixin[Model],
):
    """Media mixin."""

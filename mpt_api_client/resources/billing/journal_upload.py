from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import AsyncFileOperationsMixin, FileOperationsMixin
from mpt_api_client.models import Model


class JournalUpload(Model):
    """Journal Upload resource."""


class JournalUploadServiceConfig:
    """Journal Upload service configuration."""

    _endpoint = "/public/v1/billing/journals/{journal_id}/upload"
    _model_class = JournalUpload
    _collection_key = "data"


class JournalUploadService(
    FileOperationsMixin[JournalUpload],
    Service[JournalUpload],
    JournalUploadServiceConfig,
):
    """Journal Upload service."""


class AsyncJournalUploadService(
    AsyncFileOperationsMixin[JournalUpload],
    AsyncService[JournalUpload],
    JournalUploadServiceConfig,
):
    """Journal Upload service."""

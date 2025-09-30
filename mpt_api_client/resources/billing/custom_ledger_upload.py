from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import AsyncFileOperationsMixin, FileOperationsMixin
from mpt_api_client.models import Model


class CustomLedgerUpload(Model):
    """Custom Ledger Upload resource."""


class CustomLedgerUploadServiceConfig:
    """Custom Ledger Upload service configuration."""

    _endpoint = "/public/v1/billing/custom-ledgers/{custom_ledger_id}/upload"
    _model_class = CustomLedgerUpload
    _collection_key = "data"


class CustomLedgerUploadService(
    FileOperationsMixin[CustomLedgerUpload],
    Service[CustomLedgerUpload],
    CustomLedgerUploadServiceConfig,
):
    """Custom Ledger Upload service."""


class AsyncCustomLedgerUploadService(
    AsyncFileOperationsMixin[CustomLedgerUpload],
    AsyncService[CustomLedgerUpload],
    CustomLedgerUploadServiceConfig,
):
    """Async Custom Ledger Upload service."""

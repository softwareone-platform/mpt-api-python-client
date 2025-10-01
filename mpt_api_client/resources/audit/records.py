from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCreateMixin,
    CreateMixin,
)
from mpt_api_client.models import Model


class Record(Model):
    """Record resource."""


class RecordsServiceConfig:
    """Records service configuration."""

    _endpoint = "/public/v1/audit/records"
    _model_class = Record
    _collection_key = "data"


class RecordsService(CreateMixin[Record], Service[Record], RecordsServiceConfig):
    """Records service."""


class AsyncRecordsService(AsyncCreateMixin[Record], AsyncService[Record], RecordsServiceConfig):
    """Async records service."""

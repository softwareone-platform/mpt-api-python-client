from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    CollectionMixin,
)
from mpt_api_client.models import Model


class ExtensionTermVariant(Model):
    """Extension Term Variant resource (stub)."""


class ExtensionTermVariantsServiceConfig:
    """Extension Term Variants service configuration."""

    _endpoint = "/public/v1/integration/extensions/{extension_id}/terms/{term_id}/variants"
    _model_class = ExtensionTermVariant
    _collection_key = "data"


class ExtensionTermVariantsService(
    CollectionMixin[ExtensionTermVariant],
    Service[ExtensionTermVariant],
    ExtensionTermVariantsServiceConfig,
):
    """Sync service for extension term variants (stub)."""


class AsyncExtensionTermVariantsService(
    AsyncCollectionMixin[ExtensionTermVariant],
    AsyncService[ExtensionTermVariant],
    ExtensionTermVariantsServiceConfig,
):
    """Async service for extension term variants (stub)."""

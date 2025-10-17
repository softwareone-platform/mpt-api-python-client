from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncCreateMixin,
    AsyncGetMixin,
    AsyncUpdateMixin,
    CollectionMixin,
    CreateMixin,
    GetMixin,
    UpdateMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.resources.accounts.mixins import AsyncBlockableMixin, BlockableMixin


class ErpLink(Model):
    """ERP Link Model."""


class ErpLinksServiceConfig:
    """ERP Links Service Configuration."""

    _endpoint = "/public/v1/accounts/erp-links"
    _model_class = ErpLink
    _collection_key = "data"


class ErpLinksService(
    CreateMixin[ErpLink],
    UpdateMixin[ErpLink],
    BlockableMixin[ErpLink],
    GetMixin[ErpLink],
    CollectionMixin[ErpLink],
    Service[ErpLink],
    ErpLinksServiceConfig,
):
    """ERP Links Service."""


class AsyncErpLinksService(
    AsyncCreateMixin[ErpLink],
    AsyncUpdateMixin[ErpLink],
    AsyncBlockableMixin[ErpLink],
    AsyncGetMixin[ErpLink],
    AsyncCollectionMixin[ErpLink],
    AsyncService[ErpLink],
    ErpLinksServiceConfig,
):
    """Async ERP Links Service."""

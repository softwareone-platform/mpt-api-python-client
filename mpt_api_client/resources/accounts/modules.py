from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncGetMixin,
    CollectionMixin,
    GetMixin,
)
from mpt_api_client.models import Model


class Module(Model):
    """Module Model."""


class ModulesServiceConfig:
    """Modules Service Configuration."""

    _endpoint = "/public/v1/accounts/modules"
    _model_class = Module
    _collection_key = "data"


class ModulesService(
    GetMixin[Module], CollectionMixin[Module], Service[Module], ModulesServiceConfig
):
    """Modules Service."""


class AsyncModulesService(
    AsyncGetMixin[Module], AsyncCollectionMixin[Module], AsyncService[Module], ModulesServiceConfig
):
    """Asynchronous Modules Service."""

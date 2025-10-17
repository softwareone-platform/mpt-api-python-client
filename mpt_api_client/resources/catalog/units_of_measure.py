from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model


class UnitOfMeasure(Model):
    """Unit of Measure resource."""


class UnitsOfMeasureServiceConfig:
    """Units of Measure service configuration."""

    _endpoint = "/public/v1/catalog/units-of-measure"
    _model_class = UnitOfMeasure
    _collection_key = "data"


class UnitsOfMeasureService(
    ManagedResourceMixin[UnitOfMeasure],
    CollectionMixin[UnitOfMeasure],
    Service[UnitOfMeasure],
    UnitsOfMeasureServiceConfig,
):
    """Units of Measure service."""


class AsyncUnitsOfMeasureService(
    AsyncManagedResourceMixin[UnitOfMeasure],
    AsyncCollectionMixin[UnitOfMeasure],
    AsyncService[UnitOfMeasure],
    UnitsOfMeasureServiceConfig,
):
    """Units of Measure service."""

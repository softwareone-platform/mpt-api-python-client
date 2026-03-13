from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCollectionMixin,
    AsyncManagedResourceMixin,
    CollectionMixin,
    ManagedResourceMixin,
)
from mpt_api_client.models import Model
from mpt_api_client.models.model import BaseModel


class UnitOfMeasure(Model):
    """Unit of Measure resource.

    Attributes:
        description: Unit of measure description.
        name: Unit of measure name.
        statistics: Unit of measure statistics.
        audit: Audit information (created, updated events).
    """

    description: str | None
    name: str | None
    statistics: BaseModel | None
    audit: BaseModel | None


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

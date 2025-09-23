from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCreateMixin,
    AsyncDeleteMixin,
    AsyncUpdateMixin,
    CreateMixin,
    DeleteMixin,
    UpdateMixin,
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
    CreateMixin[UnitOfMeasure],
    DeleteMixin,
    UpdateMixin[UnitOfMeasure],
    Service[UnitOfMeasure],
    UnitsOfMeasureServiceConfig,
):
    """Units of Measure service."""


class AsyncUnitsOfMeasureService(
    AsyncCreateMixin[UnitOfMeasure],
    AsyncDeleteMixin,
    AsyncUpdateMixin[UnitOfMeasure],
    AsyncService[UnitOfMeasure],
    UnitsOfMeasureServiceConfig,
):
    """Units of Measure service."""

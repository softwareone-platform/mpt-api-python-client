import pytest

from mpt_api_client.models.model import BaseModel
from mpt_api_client.resources.catalog.units_of_measure import (
    AsyncUnitsOfMeasureService,
    UnitOfMeasure,
    UnitsOfMeasureService,
)


@pytest.fixture
def units_of_measure_service(http_client):
    return UnitsOfMeasureService(http_client=http_client)


@pytest.fixture
def async_units_of_measure_service(async_http_client):
    return AsyncUnitsOfMeasureService(http_client=async_http_client)


@pytest.fixture
def unit_of_measure_data():
    return {
        "id": "UOM-001",
        "description": "A single unit",
        "name": "Each",
        "statistics": {"items": 100},
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate"])
def test_mixins_present(units_of_measure_service, method):
    result = hasattr(units_of_measure_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate"])
def test_async_mixins_present(async_units_of_measure_service, method):
    result = hasattr(async_units_of_measure_service, method)

    assert result is True


def test_unit_of_measure_primitive_fields(unit_of_measure_data):
    result = UnitOfMeasure(unit_of_measure_data)

    assert result.to_dict() == unit_of_measure_data


def test_unit_of_measure_nested_models(unit_of_measure_data):
    result = UnitOfMeasure(unit_of_measure_data)

    assert isinstance(result.statistics, BaseModel)
    assert isinstance(result.audit, BaseModel)


def test_unit_of_measure_optional_fields_absent():
    result = UnitOfMeasure({"id": "UOM-001"})

    assert result.id == "UOM-001"
    assert not hasattr(result, "name")
    assert not hasattr(result, "description")
    assert not hasattr(result, "audit")

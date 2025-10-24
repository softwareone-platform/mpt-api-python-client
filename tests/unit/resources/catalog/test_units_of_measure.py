import pytest

from mpt_api_client.resources.catalog.units_of_measure import (
    AsyncUnitsOfMeasureService,
    UnitsOfMeasureService,
)


@pytest.fixture
def units_of_measure_service(http_client):
    return UnitsOfMeasureService(http_client=http_client)


@pytest.fixture
def async_units_of_measure_service(async_http_client):
    return AsyncUnitsOfMeasureService(http_client=async_http_client)


@pytest.mark.parametrize("method", ["get", "create", "update", "delete"])
def test_mixins_present(units_of_measure_service, method):
    assert hasattr(units_of_measure_service, method)


@pytest.mark.parametrize("method", ["get", "create", "update", "delete"])
def test_async_mixins_present(async_units_of_measure_service, method):
    assert hasattr(async_units_of_measure_service, method)

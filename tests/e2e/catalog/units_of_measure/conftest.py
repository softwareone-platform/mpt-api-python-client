import pytest


@pytest.fixture
def units_of_measure_service(mpt_ops):
    return mpt_ops.catalog.units_of_measure


@pytest.fixture
def unit_of_measure_id(e2e_config):
    return e2e_config["catalog.unit.id"]

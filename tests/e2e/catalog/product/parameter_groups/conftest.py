import pytest


@pytest.fixture
def parameter_group_id(e2e_config):
    return e2e_config["catalog.product.parameter_group.id"]


@pytest.fixture
def parameter_group_data():
    return {
        "name": "e2e - please delete",
        "label": "e2e - please delete",
        "displayOrder": 100,
    }

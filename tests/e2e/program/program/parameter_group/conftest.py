import pytest


@pytest.fixture
def parameter_group_id(e2e_config):
    return e2e_config["program.parameter.group.id"]


@pytest.fixture
def invalid_parameter_group_id():
    return "PPG-0000-0000-0000"


@pytest.fixture
def parameter_group_data():
    return {
        "name": "E2E Created Program Parameter Group",
        "description": "E2E Created Program Parameter Group",
        "label": "E2E Created Program Parameter Group",
        "default": False,
        "displayOrder": 100,
    }

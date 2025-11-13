import pytest


@pytest.fixture
def parameter_group_data():
    return {
        "name": "e2e - please delete",
        "label": "e2e - please delete",
        "displayOrder": 100,
    }

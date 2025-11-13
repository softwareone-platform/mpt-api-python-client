import pytest


@pytest.fixture
def parameter_data(parameter_group_id):
    return {
        "constraints": {"hidden": False, "readonly": False, "required": False},
        "description": "e2e - please delete",
        "displayOrder": 100,
        "name": "e2e - please delete",
        "phase": "Order",
        "scope": "Order",
        "type": "SingleLineText",
        "context": "Purchase",
        "options": {
            "hintText": "delete",
            "defaultValue": "Delete me",
            "placeholderText": "Place holder text",
        },
        "group": {"id": parameter_group_id},
    }

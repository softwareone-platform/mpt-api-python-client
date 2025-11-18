import pytest


@pytest.fixture
def item_group_data(product_id):
    return {
        "product": {"id": product_id},
        "name": "e2e - please delete",
        "label": "e2e - please delete",
        "description": "e2e - temporary item group",
        "displayOrder": 100,
        "default": False,
        "multiple": True,
        "required": True,
    }

import pytest


@pytest.fixture
def item_data(short_uuid, product_id, item_group_id, unit_id):
    return {
        "name": "e2e - please delete",
        "description": "e2e - please delete",
        "unit": {
            "id": unit_id,
        },
        "group": {
            "id": item_group_id,
        },
        "product": {
            "id": product_id,
        },
        "terms": {"model": "quantity", "period": "1m", "commitment": "1m"},
        "externalIds": {"vendor": f"e2e-delete-{short_uuid}"},
    }

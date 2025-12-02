import pytest


@pytest.fixture
def category_data(short_uuid):
    return {
        "name": f"e2e-category-{short_uuid}",
        "description": "E2E test category - please delete",
        "externalId": f"e2e-cat-{short_uuid}",
    }


@pytest.fixture
def invalid_category_id():
    return "NCT-000-000-000"

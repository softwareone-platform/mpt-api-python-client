import pytest


@pytest.fixture
def category_data(short_uuid):
    return {
        "name": f"e2e-category-{short_uuid}",
        "description": "E2E test category - please delete",
        "externalId": f"e2e-cat-{short_uuid}",
    }

import pytest


@pytest.fixture
def category_id(e2e_config):
    return e2e_config["notifications.category.id"]

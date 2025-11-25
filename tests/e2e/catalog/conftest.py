import pytest


@pytest.fixture
def item_id(e2e_config):
    return e2e_config.get("catalog.product.item.id")


@pytest.fixture
def item_group_id(e2e_config):
    return e2e_config.get("catalog.product.item_group.id")


@pytest.fixture
def unit_id(e2e_config):
    return e2e_config.get("catalog.unit.id")

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


@pytest.fixture
def authorization_id(e2e_config):
    return e2e_config["catalog.authorization.id"]


@pytest.fixture
def price_list_id(e2e_config):
    return e2e_config["catalog.price_list.id"]

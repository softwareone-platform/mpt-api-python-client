import pytest


@pytest.fixture
def agreement_id(e2e_config):
    return e2e_config["commerce.agreement.id"]


@pytest.fixture
def commerce_product_id(e2e_config):
    return e2e_config["commerce.product.id"]


@pytest.fixture
def asset_item_id(e2e_config):
    return e2e_config["commerce.assets.product.item.id"]


@pytest.fixture
def asset_agreement_id(e2e_config):
    return e2e_config["commerce.assets.agreement.id"]

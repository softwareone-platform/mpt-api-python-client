import pytest


@pytest.fixture
def agreement_id(e2e_config):
    return e2e_config["commerce.agreement.id"]


@pytest.fixture
def commerce_product_id(e2e_config):
    return e2e_config["commerce.product.id"]


@pytest.fixture
def subscription_item_id(e2e_config):
    return e2e_config["commerce.subscription.product.item.id"]


@pytest.fixture
def subscription_agreement_id(e2e_config):
    return e2e_config["commerce.subscription.agreement.id"]

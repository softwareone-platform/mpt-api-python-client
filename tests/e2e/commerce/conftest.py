import pytest


@pytest.fixture
def agreement_id(e2e_config):
    return e2e_config["commerce.agreement.id"]


@pytest.fixture
def commerce_product_id(e2e_config):
    return e2e_config["commerce.product.id"]


@pytest.fixture
def order_id(e2e_config):
    return e2e_config["commerce.order.id"]


@pytest.fixture
def commerce_item_id(e2e_config):
    return e2e_config["commerce.product.item.id"]


@pytest.fixture
def commerce_product_template_id(e2e_config):
    return e2e_config["commerce.product.template.id"]


@pytest.fixture
def commerce_user_id(e2e_config):
    return e2e_config["commerce.user.id"]

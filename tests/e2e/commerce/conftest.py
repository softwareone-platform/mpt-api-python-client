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


@pytest.fixture
def subscription_item_id(e2e_config):
    return e2e_config["commerce.subscription.product.item.id"]


@pytest.fixture
def subscription_agreement_id(e2e_config):
    return e2e_config["commerce.subscription.agreement.id"]


@pytest.fixture
def asset_item_id(e2e_config):
    return e2e_config["commerce.assets.product.item.id"]


@pytest.fixture
def asset_agreement_id(e2e_config):
    return e2e_config["commerce.assets.agreement.id"]


@pytest.fixture
def subscription_id(e2e_config):
    return e2e_config["commerce.subscription.id"]


@pytest.fixture
def agreement_subscription_line_id(e2e_config):
    return e2e_config["commerce.agreement.subscription.line.id"]


@pytest.fixture
def invalid_subscription_id():
    return "SUB-0000-0000-0000"


@pytest.fixture
def asset_id(e2e_config):
    return e2e_config["commerce.assets.id"]


@pytest.fixture
def invalid_asset_id():
    return "AST-0000-0000-0000"

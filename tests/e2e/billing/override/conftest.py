import pytest


@pytest.fixture
def billing_override_id(e2e_config):
    return e2e_config["billing.override.id"]


@pytest.fixture
def invalid_billing_override_id():
    return "BOV-0000-0000"

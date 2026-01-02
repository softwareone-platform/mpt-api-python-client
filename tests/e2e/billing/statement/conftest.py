import pytest


@pytest.fixture
def billing_statement_id(e2e_config):
    return e2e_config["billing.statement.id"]


@pytest.fixture
def invalid_billing_statement_id():
    return "STM-0000-0000"

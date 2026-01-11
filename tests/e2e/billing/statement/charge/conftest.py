import pytest


@pytest.fixture
def statement_charge_id(e2e_config):
    return e2e_config["billing.statement.charge.id"]


@pytest.fixture
def invalid_statement_charge_id():
    return "CHG-0000-0000-0000-0000-0000"

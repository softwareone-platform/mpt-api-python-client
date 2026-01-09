import pytest


@pytest.fixture
def ledger_charge_id(e2e_config):
    return e2e_config["billing.ledger.charge.id"]


@pytest.fixture
def invalid_ledger_charge_id():
    return "CHG-0000-0000-0000-0000-0000"

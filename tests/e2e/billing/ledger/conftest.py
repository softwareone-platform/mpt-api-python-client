import pytest


@pytest.fixture
def ledger_id(e2e_config):
    return e2e_config["billing.ledger.id"]


@pytest.fixture
def invalid_ledger_id():
    return "BLE-0000-0000-0000-0000"

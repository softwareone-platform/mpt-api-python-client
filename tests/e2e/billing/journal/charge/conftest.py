import pytest


@pytest.fixture
def journal_charge_id(e2e_config):
    return e2e_config["billing.journal.charge.id"]


@pytest.fixture
def invalid_journal_charge_id():
    return "CHG-0000-0000-0000-0000-0000"

import pytest


@pytest.fixture
def statement_id(e2e_config):
    return e2e_config["billing.statement.id"]


@pytest.fixture
def invalid_statement_id():
    return "SOM-0000-0000-0000-0000"

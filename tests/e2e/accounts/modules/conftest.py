import pytest


@pytest.fixture
def invalid_module_id():
    return "MOD-0000"


@pytest.fixture
def module_name(e2e_config):
    return e2e_config["accounts.module.name"]

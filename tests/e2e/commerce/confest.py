import pytest


@pytest.fixture
def agreement_id(e2e_config):
    return e2e_config["commerce.agreement.id"]

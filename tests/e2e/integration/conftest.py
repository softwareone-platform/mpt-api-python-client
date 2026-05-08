import pytest


@pytest.fixture
def extension_id(e2e_config):
    return e2e_config["integration.extension.id"]

import pytest


@pytest.fixture
def program_id(e2e_config):
    return e2e_config.get("program.program.id")

import pytest


@pytest.fixture
def term_id(e2e_config):
    return e2e_config["program.terms.id"]


@pytest.fixture
def invalid_term_id():
    return "PTC-0000-0000-0000"


@pytest.fixture
def term_data():
    return {
        "name": "E2E Created Program Terms",
        "description": "E2E Created Program Terms",
        "displayOrder": 100,
    }

import pytest


@pytest.fixture
def term_data():
    return {"name": "e2e - please delete", "description": "Test term description"}


@pytest.fixture
def term_id(e2e_config):
    return e2e_config["catalog.product.terms.id"]

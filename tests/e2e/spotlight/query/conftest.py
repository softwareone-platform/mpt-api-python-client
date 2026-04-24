import pytest


@pytest.fixture
def spotlight_query_id(e2e_config):
    return e2e_config["spotlight.query.id"]


@pytest.fixture
def invalid_spotlight_query_id():
    return "SPQ-0000-0000"

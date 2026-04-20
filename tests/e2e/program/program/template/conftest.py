import pytest


@pytest.fixture
def template_id(e2e_config):
    return e2e_config["program.template.id"]


@pytest.fixture
def invalid_template_id():
    return "PTM-0000-0000-0000"


@pytest.fixture
def template_data():
    return {
        "name": "E2E Created Program Template",
        "type": "EnrollmentProcessing",
        "default": False,
        "externalIds": {"vendor": None},
        "content": "E2E Created Program Template",
    }

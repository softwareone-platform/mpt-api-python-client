import pytest


@pytest.fixture
def parameter_id(e2e_config):
    return e2e_config["program.parameter.id"]


@pytest.fixture
def invalid_parameter_id():
    return "PPM-0000-0000-0000"


@pytest.fixture
def parameter_data():
    return {
        "externalId": "e2eCreatedProgramParameter",
        "displayOrder": 100,
        "scope": "Enrollment",
        "phase": "Fulfillment",
        "multiple": False,
        "description": "E2E Created Program Parameter",
        "type": "SingleLineText",
        "constraints": {"hidden": False, "required": False, "readonly": False},
        "name": "E2E Created Program Parameter",
        "options": {
            "type": "SingleLineText",
            "placeholderText": "E2E Created Program Parameter",
            "name": "E2E Created Program Parameter",
            "hintText": "E2E Created Program Parameter",
        },
    }

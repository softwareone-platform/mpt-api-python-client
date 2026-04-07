import pytest

from tests.e2e.helper import (
    async_create_fixture_resource_and_delete,
    create_fixture_resource_and_delete,
)


@pytest.fixture
def parameter_data(short_uuid):
    return {
        "name": f"E2E Helpdesk Parameter {short_uuid}",
        "description": "E2E Created Helpdesk Parameter",
        "scope": "Case",
        "phase": "Request",
        "type": "SingleLineText",
        "multiple": False,
        "constraints": {
            "required": False,
            "readonly": False,
            "hidden": False,
            "visibility": "All",
        },
    }


@pytest.fixture(scope="session")
def invalid_parameter_id():
    return "PAR-0000-0000"


@pytest.fixture
def created_parameter(mpt_ops, parameter_data):
    with create_fixture_resource_and_delete(
        mpt_ops.helpdesk.parameters, parameter_data
    ) as parameter:
        yield parameter


@pytest.fixture
async def async_created_parameter(async_mpt_ops, parameter_data):
    async with async_create_fixture_resource_and_delete(
        async_mpt_ops.helpdesk.parameters, parameter_data
    ) as parameter:
        yield parameter

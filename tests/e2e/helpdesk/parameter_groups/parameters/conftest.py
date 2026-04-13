import pytest

from tests.e2e.helper import (
    async_create_fixture_resource_and_delete,
    create_fixture_resource_and_delete,
)


@pytest.fixture
def created_parameter_definition(mpt_ops, parameter_data):
    with create_fixture_resource_and_delete(
        mpt_ops.helpdesk.parameters, parameter_data
    ) as parameter_definition:
        yield parameter_definition


@pytest.fixture
async def async_created_parameter_definition(async_mpt_ops, parameter_data):
    async with async_create_fixture_resource_and_delete(
        async_mpt_ops.helpdesk.parameters, parameter_data
    ) as parameter_definition:
        yield parameter_definition


@pytest.fixture
def parameter_group_parameters_service(mpt_ops, created_parameter_group):
    return mpt_ops.helpdesk.parameter_groups.parameters(created_parameter_group.id)


@pytest.fixture
def parameter_group_parameter_data(created_parameter_definition):
    return {
        "parameterId": created_parameter_definition.id,
        "displayOrder": 100,
    }


@pytest.fixture
def created_parameter_group_parameter(parameter_group_parameters_service, created_parameter):
    with create_fixture_resource_and_delete(
        parameter_group_parameters_service, {"id": created_parameter.id, "displayOrder": 1}
    ) as parameter_group_parameter:
        yield parameter_group_parameter


@pytest.fixture(scope="session")
def invalid_parameter_group_parameter_id():
    return "PAR-0000-0000"


@pytest.fixture
def async_parameter_group_parameters_service(async_mpt_ops, async_created_parameter_group):
    return async_mpt_ops.helpdesk.parameter_groups.parameters(async_created_parameter_group.id)


@pytest.fixture
def async_parameter_group_parameter_data(async_created_parameter_definition):
    return {
        "parameterId": async_created_parameter_definition.id,
        "displayOrder": 100,
    }


@pytest.fixture
async def async_created_parameter_group_parameter(
    async_parameter_group_parameters_service, async_created_parameter
):
    async with async_create_fixture_resource_and_delete(
        async_parameter_group_parameters_service,
        {"id": async_created_parameter.id, "displayOrder": 1},
    ) as parameter_group_parameter:
        yield parameter_group_parameter

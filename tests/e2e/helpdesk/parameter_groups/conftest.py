import pytest

from tests.e2e.helper import (
    async_create_fixture_resource_and_delete,
    create_fixture_resource_and_delete,
)


@pytest.fixture
def parameter_group_data(short_uuid):
    return {
        "name": f"E2E Helpdesk Parameter Group {short_uuid}",
        "label": f"E2E Label {short_uuid}",
        "description": "E2E Created Helpdesk Parameter Group",
    }


@pytest.fixture
def invalid_parameter_group_id():
    return "PGR-0000-0000"


@pytest.fixture
def parameter_groups_service(mpt_ops):
    return mpt_ops.helpdesk.parameter_groups


@pytest.fixture
def async_parameter_groups_service(async_mpt_ops):
    return async_mpt_ops.helpdesk.parameter_groups


@pytest.fixture
def created_parameter_group(parameter_groups_service, parameter_group_data):
    with create_fixture_resource_and_delete(
        parameter_groups_service, parameter_group_data
    ) as parameter_group:
        yield parameter_group


@pytest.fixture
async def async_created_parameter_group(async_parameter_groups_service, parameter_group_data):
    async with async_create_fixture_resource_and_delete(
        async_parameter_groups_service, parameter_group_data
    ) as parameter_group:
        yield parameter_group

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def created_parameter_group(async_mpt_vendor, program_id, parameter_group_data):
    service = async_mpt_vendor.program.programs.parameter_groups(program_id)
    group = await service.create(parameter_group_data)
    yield group
    try:
        await service.delete(group.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete parameter group {group.id}: {error.title}")  # noqa: WPS421


def test_create_parameter_group(created_parameter_group):
    result = created_parameter_group.name == "E2E Created Program Parameter Group"

    assert result is True


async def test_update_parameter_group(async_mpt_vendor, program_id, created_parameter_group):
    service = async_mpt_vendor.program.programs.parameter_groups(program_id)
    update_data = {"name": "E2E Updated Program Parameter Group"}

    result = await service.update(created_parameter_group.id, update_data)

    assert result.name == update_data["name"]


async def test_get_parameter_group(async_mpt_vendor, program_id, parameter_group_id):
    service = async_mpt_vendor.program.programs.parameter_groups(program_id)

    result = await service.get(parameter_group_id)

    assert result.id == parameter_group_id


async def test_delete_parameter_group(async_mpt_vendor, program_id, created_parameter_group):
    parameter_group_data = created_parameter_group

    result = async_mpt_vendor.program.programs.parameter_groups(program_id)

    await result.delete(parameter_group_data.id)


async def test_filter_and_select_parameter_groups(async_mpt_vendor, program_id, parameter_group_id):
    select_fields = ["-description", "-audit"]
    filtered_groups = (
        async_mpt_vendor.program.programs
        .parameter_groups(program_id)
        .filter(RQLQuery(id=parameter_group_id))
        .filter(RQLQuery(name="E2E Seeded Program Parameter Group"))
        .select(*select_fields)
    )

    result = [parameter_group async for parameter_group in filtered_groups.iterate()]

    assert len(result) == 1

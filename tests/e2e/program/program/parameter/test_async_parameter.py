import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def created_parameter(async_mpt_vendor, program_id, parameter_data):
    service = async_mpt_vendor.program.programs.parameters(program_id)
    parameter = await service.create(parameter_data)
    yield parameter
    try:
        await service.delete(parameter.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete parameter {parameter.id}: {error.title}")  # noqa: WPS421


def test_create_parameter(created_parameter):
    result = created_parameter.name == "E2E Created Program Parameter"

    assert result is True


async def test_update_parameter(async_mpt_vendor, program_id, created_parameter):
    service = async_mpt_vendor.program.programs.parameters(program_id)
    update_data = {"name": "E2E Updated Program Parameter"}

    result = await service.update(created_parameter.id, update_data)

    assert result.name == update_data["name"]


async def test_get_parameter(async_mpt_vendor, program_id, parameter_id):
    service = async_mpt_vendor.program.programs.parameters(program_id)

    result = await service.get(parameter_id)

    assert result.id == parameter_id


async def test_get_invalid_parameter(async_mpt_vendor, program_id, invalid_parameter_id):
    with pytest.raises(MPTAPIError):
        await async_mpt_vendor.program.programs.parameters(program_id).get(invalid_parameter_id)


async def test_delete_parameter(async_mpt_vendor, program_id, created_parameter):
    parameter_data = created_parameter

    result = async_mpt_vendor.program.programs.parameters(program_id)

    await result.delete(parameter_data.id)


async def test_filter_and_select_parameters(async_mpt_vendor, program_id, parameter_id):
    select_fields = ["-description", "-audit"]
    filtered_parameters = (
        async_mpt_vendor.program.programs
        .parameters(program_id)
        .filter(RQLQuery(id=parameter_id))
        .filter(RQLQuery(name="E2E Seeded Program Parameter"))
        .select(*select_fields)
    )

    result = [parameter async for parameter in filtered_parameters.iterate()]

    assert len(result) == 1

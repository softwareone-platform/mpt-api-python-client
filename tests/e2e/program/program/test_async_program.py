import pytest

from mpt_api_client import RQLQuery
from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def created_program(async_mpt_vendor, program_data, logo_fd):
    program = await async_mpt_vendor.program.programs.create(program_data, file=logo_fd)

    yield program

    try:
        await async_mpt_vendor.program.programs.delete(program.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete program {program.id}: {error.title}")  # noqa: WPS421


def test_create_program(created_program, program_data):
    result = created_program.name == program_data["name"]

    assert result is True


async def test_update_program(async_mpt_vendor, created_program):
    update_data = {"name": "E2E Updated Program"}

    result = await async_mpt_vendor.program.programs.update(created_program.id, update_data)

    assert result.name == update_data["name"]


async def test_get_program(async_mpt_vendor, program_id):
    result = await async_mpt_vendor.program.programs.get(program_id)

    assert result.id == program_id


async def test_filter_and_select_programs(async_mpt_vendor, program_id):
    select_fields = ["-icon", "-revision", "-audit"]
    filtered_programs = (
        async_mpt_vendor.program.programs
        .filter(RQLQuery(id=program_id))
        .filter(RQLQuery(name="E2E Seeded Program"))
        .select(*select_fields)
    )

    result = [program async for program in filtered_programs.iterate()]

    assert len(result) == 1


async def test_delete_program(async_mpt_vendor, created_program):
    program_data = created_program

    result = async_mpt_vendor.program.programs

    await result.delete(program_data.id)


async def test_publish_program(async_mpt_vendor, created_program):
    result = await async_mpt_vendor.program.programs.publish(created_program.id)

    assert result is not None


async def test_unpublish_program(async_mpt_vendor, created_program):
    await async_mpt_vendor.program.programs.publish(created_program.id)

    result = await async_mpt_vendor.program.programs.unpublish(created_program.id)

    assert result is not None

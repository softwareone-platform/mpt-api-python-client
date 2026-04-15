import pytest

from mpt_api_client import RQLQuery
from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_program(mpt_vendor, program_data, logo_fd):
    program = mpt_vendor.program.programs.create(program_data, file=logo_fd)

    yield program

    try:
        mpt_vendor.program.programs.delete(program.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete program {program.id}: {error.title}")  # noqa: WPS421


def test_create_program(created_program, program_data):
    result = created_program.name == program_data["name"]

    assert result is True


def test_update_program(mpt_vendor, created_program):
    update_data = {"name": "E2E Updated Program"}

    result = mpt_vendor.program.programs.update(created_program.id, update_data)

    assert result.name == update_data["name"]


def test_get_program(mpt_vendor, program_id):
    result = mpt_vendor.program.programs.get(program_id)

    assert result.id == program_id


def test_filter_and_select_programs(mpt_vendor, program_id):
    select_fields = ["-icon", "-revision", "-audit"]
    filtered_programs = (
        mpt_vendor.program.programs
        .filter(RQLQuery(id=program_id))
        .filter(RQLQuery(name="E2E Seeded Program"))
        .select(*select_fields)
    )

    result = list(filtered_programs.iterate())

    assert len(result) == 1


def test_delete_program(mpt_vendor, created_program):
    program_data = created_program

    result = mpt_vendor.program.programs

    result.delete(program_data.id)


def test_publish_program(mpt_vendor, created_program):
    result = mpt_vendor.program.programs.publish(created_program.id)

    assert result is not None


def test_unpublish_program(mpt_vendor, created_program):
    mpt_vendor.program.programs.publish(created_program.id)

    result = mpt_vendor.program.programs.unpublish(created_program.id)

    assert result is not None

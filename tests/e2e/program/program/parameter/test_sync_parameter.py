import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery
from tests.e2e.program.program.parameter.conftest import EXTERNAL_ID

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_parameter(mpt_vendor, program_id, parameter_data):
    service = mpt_vendor.program.programs.parameters(program_id)
    try:
        parameter = service.create(parameter_data)
    except MPTAPIError as error:
        if (
            error.status_code == 400
            and error.detail
            and f"Parameter with given external identifier '{EXTERNAL_ID}' already "
            "exists for given program."
            in error.detail
        ):
            parameter = service.filter(RQLQuery(externalId=EXTERNAL_ID)).fetch_one()
        else:
            raise
    yield parameter
    try:
        service.delete(parameter.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete parameter {parameter.id}: {error.title}")  # noqa: WPS421


def test_create_parameter(created_parameter):
    result = created_parameter.name == "E2E Created Program Parameter"

    assert result is True


def test_update_parameter(mpt_vendor, program_id, created_parameter):
    service = mpt_vendor.program.programs.parameters(program_id)
    update_data = {"name": "E2E Updated Program Parameter"}

    result = service.update(created_parameter.id, update_data)

    assert result.name == update_data["name"]


def test_get_parameter(mpt_vendor, program_id, parameter_id):
    service = mpt_vendor.program.programs.parameters(program_id)

    result = service.get(parameter_id)

    assert result.id == parameter_id


def test_get_invalid_parameter(mpt_vendor, program_id, invalid_parameter_id):
    with pytest.raises(MPTAPIError):
        mpt_vendor.program.programs.parameters(program_id).get(invalid_parameter_id)


def test_delete_parameter(mpt_vendor, program_id, created_parameter):
    parameter_data = created_parameter

    result = mpt_vendor.program.programs.parameters(program_id)

    result.delete(parameter_data.id)


def test_filter_and_select_parameters(mpt_vendor, program_id, parameter_id):
    select_fields = ["-description", "-audit"]
    filtered_parameters = (
        mpt_vendor.program.programs
        .parameters(program_id)
        .filter(RQLQuery(id=parameter_id))
        .filter(RQLQuery(name="E2E Seeded Program Parameter"))
        .select(*select_fields)
    )

    result = list(filtered_parameters.iterate())

    assert len(result) == 1

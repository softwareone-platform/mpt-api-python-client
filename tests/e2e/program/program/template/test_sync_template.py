import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_template(mpt_vendor, program_id, template_data):
    service = mpt_vendor.program.programs.templates(program_id)
    template = service.create(template_data)
    yield template
    try:
        service.delete(template.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete template {template.id}: {error.title}")  # noqa: WPS421


def test_create_template(created_template):
    result = created_template.name == "E2E Created Program Template"

    assert result is True


def test_update_template(mpt_vendor, program_id, created_template):
    service = mpt_vendor.program.programs.templates(program_id)
    update_data = {"name": "E2E Updated Program Template"}

    result = service.update(created_template.id, update_data)

    assert result.name == update_data["name"]


def test_get_template(mpt_vendor, program_id, template_id):
    service = mpt_vendor.program.programs.templates(program_id)

    result = service.get(template_id)

    assert result.id == template_id


def test_get_template_invalid_id(mpt_vendor, program_id, invalid_template_id):
    with pytest.raises(MPTAPIError):
        mpt_vendor.program.programs.templates(program_id).get(invalid_template_id)


def test_delete_template(mpt_vendor, program_id, created_template):
    template_data = created_template

    result = mpt_vendor.program.programs.templates(program_id)

    result.delete(template_data.id)


def test_filter_and_select_templates(mpt_vendor, program_id, template_id):
    select_fields = ["-content", "-audit"]
    filtered_templates = (
        mpt_vendor.program.programs
        .templates(program_id)
        .filter(RQLQuery(id=template_id))
        .filter(RQLQuery(name="E2E Seeded Program Template"))
        .select(*select_fields)
    )

    result = list(filtered_templates.iterate())

    assert len(result) == 1

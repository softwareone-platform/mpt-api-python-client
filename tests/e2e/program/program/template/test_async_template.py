import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def created_template(async_mpt_vendor, program_id, template_data):
    service = async_mpt_vendor.program.programs.templates(program_id)
    template = await service.create(template_data)
    yield template
    try:
        await service.delete(template.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete template {template.id}: {error.title}")  # noqa: WPS421


def test_create_template(created_template):
    result = created_template.name == "E2E Created Program Template"

    assert result is True


async def test_update_template(async_mpt_vendor, program_id, created_template):
    service = async_mpt_vendor.program.programs.templates(program_id)
    update_data = {"name": "E2E Updated Program Template"}

    result = await service.update(created_template.id, update_data)

    assert result.name == update_data["name"]


async def test_get_template(async_mpt_vendor, program_id, template_id):
    service = async_mpt_vendor.program.programs.templates(program_id)

    result = await service.get(template_id)

    assert result.id == template_id


async def test_get_template_invalid_id(async_mpt_vendor, program_id, invalid_template_id):
    with pytest.raises(MPTAPIError):
        await async_mpt_vendor.program.programs.templates(program_id).get(invalid_template_id)


async def test_delete_template(async_mpt_vendor, program_id, created_template):
    template_data = created_template

    result = async_mpt_vendor.program.programs.templates(program_id)

    await result.delete(template_data.id)


async def test_filter_and_select_templates(async_mpt_vendor, program_id, template_id):
    select_fields = ["-content", "-audit"]
    filtered_templates = (
        async_mpt_vendor.program.programs
        .templates(program_id)
        .filter(RQLQuery(id=template_id))
        .filter(RQLQuery(name="E2E Seeded Program Template"))
        .select(*select_fields)
    )

    result = [template async for template in filtered_templates.iterate()]

    assert len(result) == 1

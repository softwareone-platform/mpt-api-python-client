import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def created_term(async_mpt_vendor, program_id, term_data):
    service = async_mpt_vendor.program.programs.terms(program_id)
    term = await service.create(term_data)
    yield term
    try:
        await service.delete(term.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete term {term.id}: {error.title}")  # noqa: WPS421


def test_create_term(created_term):
    result = created_term.name == "E2E Created Program Terms"

    assert result is True


async def test_update_term(async_mpt_vendor, program_id, created_term):
    service = async_mpt_vendor.program.programs.terms(program_id)
    update_data = {"name": "E2E Updated Program Terms"}

    result = await service.update(created_term.id, update_data)

    assert result.name == update_data["name"]


async def test_get_term(async_mpt_vendor, program_id, term_id):
    service = async_mpt_vendor.program.programs.terms(program_id)

    result = await service.get(term_id)

    assert result.id == term_id


async def test_get_invalid_term(async_mpt_vendor, program_id, invalid_term_id):
    with pytest.raises(MPTAPIError):
        await async_mpt_vendor.program.programs.terms(program_id).get(invalid_term_id)


async def test_delete_term(async_mpt_vendor, program_id, created_term):
    term_data = created_term

    result = async_mpt_vendor.program.programs.terms(program_id)

    await result.delete(term_data.id)


async def test_filter_and_select_terms(async_mpt_vendor, program_id, term_id):
    select_fields = ["-description", "-audit"]
    filtered_terms = (
        async_mpt_vendor.program.programs
        .terms(program_id)
        .filter(RQLQuery(id=term_id))
        .filter(RQLQuery(name="E2E Seeded Program Terms"))
        .select(*select_fields)
    )

    result = [terms async for terms in filtered_terms.iterate()]

    assert len(result) == 1


async def test_publish_term(async_mpt_vendor, program_id, created_term):
    service = async_mpt_vendor.program.programs.terms(program_id)

    result = await service.publish(created_term.id)

    assert result.status == "Published"


async def test_unpublish_term(async_mpt_vendor, program_id, created_term):
    service = async_mpt_vendor.program.programs.terms(program_id)
    await service.publish(created_term.id)

    result = await service.unpublish(created_term.id)

    assert result.status == "Unpublished"

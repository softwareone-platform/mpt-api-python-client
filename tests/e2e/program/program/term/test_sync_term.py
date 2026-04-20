import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_term(mpt_vendor, program_id, term_data):
    service = mpt_vendor.program.programs.terms(program_id)
    term = service.create(term_data)
    yield term
    try:
        service.delete(term.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete term {term.id}: {error.title}")  # noqa: WPS421


def test_create_term(created_term):
    result = created_term.name == "E2E Created Program Terms"

    assert result is True


def test_update_term(mpt_vendor, program_id, created_term):
    service = mpt_vendor.program.programs.terms(program_id)
    update_data = {"name": "E2E Updated Program Terms"}

    result = service.update(created_term.id, update_data)

    assert result.name == update_data["name"]


def test_get_term(mpt_vendor, program_id, term_id):
    service = mpt_vendor.program.programs.terms(program_id)

    result = service.get(term_id)

    assert result.id == term_id


def test_get_invalid_term(mpt_vendor, program_id, invalid_term_id):
    with pytest.raises(MPTAPIError):
        mpt_vendor.program.programs.terms(program_id).get(invalid_term_id)


def test_delete_term(mpt_vendor, program_id, created_term):
    term_data = created_term

    result = mpt_vendor.program.programs.terms(program_id)

    result.delete(term_data.id)


def test_filter_and_select_terms(mpt_vendor, program_id, term_id):
    select_fields = ["-description", "-audit"]
    filtered_terms = (
        mpt_vendor.program.programs
        .terms(program_id)
        .filter(RQLQuery(id=term_id))
        .filter(RQLQuery(name="E2E Seeded Program Terms"))
        .select(*select_fields)
    )

    result = list(filtered_terms.iterate())

    assert len(result) == 1


def test_publish_term(mpt_vendor, program_id, created_term):
    service = mpt_vendor.program.programs.terms(program_id)

    result = service.publish(created_term.id)

    assert result.status == "Published"


def test_unpublish_term(mpt_vendor, program_id, created_term):
    service = mpt_vendor.program.programs.terms(program_id)
    service.publish(created_term.id)

    result = service.unpublish(created_term.id)

    assert result.status == "Unpublished"

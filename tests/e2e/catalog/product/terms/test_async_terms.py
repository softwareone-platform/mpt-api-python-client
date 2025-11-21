import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def async_vendor_terms_service(async_mpt_vendor, product_id):
    return async_mpt_vendor.catalog.products.terms(product_id)


@pytest.fixture
async def async_created_term(async_vendor_terms_service, term_data):
    service = async_vendor_terms_service
    term = await service.create(term_data)
    yield term
    try:
        await service.delete(term.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete term {term.id}: {error.title}")


def test_create_term(async_created_term):
    term = async_created_term
    assert term.name == "e2e - please delete"


async def test_update_term(async_vendor_terms_service, async_created_term):
    service = async_vendor_terms_service
    update_data = {"name": "e2e - delete me (updated)"}
    term = await service.update(async_created_term.id, update_data)
    assert term.name == "e2e - delete me (updated)"


async def test_get_term(async_vendor_terms_service, term_id):
    service = async_vendor_terms_service
    term = await service.get(term_id)
    assert term.id == term_id


async def test_get_term_by_id(async_vendor_terms_service, term_id):
    service = async_vendor_terms_service
    term = await service.get(term_id)
    assert term.id == term_id


async def test_iterate_terms(async_vendor_terms_service, async_created_term):
    service = async_vendor_terms_service
    terms = [term async for term in service.iterate()]
    assert any(term.id == async_created_term.id for term in terms)


async def test_filter_terms(async_vendor_terms_service, term_id):
    select_fields = ["-description"]
    filtered_terms = async_vendor_terms_service.filter(RQLQuery(id=term_id)).select(*select_fields)
    terms = [term async for term in filtered_terms.iterate()]
    assert len(terms) == 1
    assert terms[0].id == term_id


async def test_delete_term(async_vendor_terms_service, async_created_term):
    service = async_vendor_terms_service
    await service.delete(async_created_term.id)
    with pytest.raises(MPTAPIError):
        await service.get(async_created_term.id)

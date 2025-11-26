import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def vendor_terms_service(mpt_vendor, product_id):
    return mpt_vendor.catalog.products.terms(product_id)


@pytest.fixture
def created_term(logger, vendor_terms_service, term_data):
    service = vendor_terms_service
    term = service.create(term_data)
    yield term
    try:
        service.delete(term.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete term {term.id}: {error.title}")


@pytest.fixture
def created_term_from_url(logger, vendor_terms_service, term_data, pdf_url):
    term_data["url"] = pdf_url
    service = vendor_terms_service
    term = service.create(term_data)
    yield term
    try:
        service.delete(term.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete term {term.id}: {error.title}")


def test_create_term(created_term):
    result = created_term

    assert result.name == "e2e - please delete"


def test_update_term(vendor_terms_service, created_term):
    service = vendor_terms_service
    update_data = {"name": "e2e - delete me (updated)"}

    result = service.update(created_term.id, update_data)

    assert result.name == "e2e - delete me (updated)"


def test_get_term(vendor_terms_service, term_id):
    service = vendor_terms_service

    result = service.get(term_id)

    assert result.id == term_id


def test_get_term_by_id(vendor_terms_service, term_id):
    service = vendor_terms_service

    result = service.get(term_id)

    assert result.id == term_id


def test_iterate_terms(vendor_terms_service, created_term):
    service = vendor_terms_service

    result = list(service.iterate())

    assert any(term.id == created_term.id for term in result)


def test_filter_terms(vendor_terms_service, term_id):
    select_fields = ["-description"]
    filtered_terms = vendor_terms_service.filter(RQLQuery(id=term_id)).select(*select_fields)

    result = list(filtered_terms.iterate())

    assert len(result) == 1
    assert result[0].id == term_id


def test_delete_term(vendor_terms_service, created_term):
    service = vendor_terms_service

    service.delete(created_term.id)  # act

    with pytest.raises(MPTAPIError):
        service.get(created_term.id)

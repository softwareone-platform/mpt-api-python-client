import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def vendor_variant_service(mpt_vendor, product_id, term_id):
    return mpt_vendor.catalog.products.terms(product_id).variants(term_id)


@pytest.fixture
def created_variant(vendor_variant_service, variant_data, pdf_fd):
    variant = vendor_variant_service.create(variant_data, pdf_fd)
    yield variant
    try:
        vendor_variant_service.delete(variant.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete variant {variant.id}: {error.title}")


@pytest.fixture
def created_variant_from_url(vendor_variant_service, variant_data, pdf_url):
    variant_data["type"] = "Online"
    variant_data["assetUrl"] = pdf_url
    variant = vendor_variant_service.create(variant_data)
    yield variant
    try:
        vendor_variant_service.delete(variant.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete variant {variant.id}: {error.title}")


def test_create_variant(created_variant, variant_data):
    result = created_variant.name == variant_data["name"]

    assert result is True


def test_create_variant_from_url(created_variant_from_url, variant_data):
    result = created_variant_from_url.name == variant_data["name"]

    assert result is True


def test_update_variant(vendor_variant_service, created_variant):
    update_data = {"name": "e2e - delete me (updated)"}

    result = vendor_variant_service.update(created_variant.id, update_data)

    assert result.name == "e2e - delete me (updated)"


def test_get_variant(vendor_variant_service, variant_id):
    result = vendor_variant_service.get(variant_id)

    assert result.id == variant_id


def test_get_variant_by_id(vendor_variant_service, variant_id):
    result = vendor_variant_service.get(variant_id)

    assert result.id == variant_id


def test_iterate_variants(vendor_variant_service, created_variant):
    result = list(vendor_variant_service.iterate())

    assert any(variant.id == created_variant.id for variant in result)


def test_filter_variants(vendor_variant_service, variant_id):
    select_fields = ["-description"]
    filtered_variants = vendor_variant_service.filter(RQLQuery(id=variant_id)).select(
        *select_fields
    )

    result = list(filtered_variants.iterate())

    assert len(result) == 1
    assert result[0].id == variant_id


def test_delete_variant(vendor_variant_service, created_variant):
    vendor_variant_service.delete(created_variant.id)

    with pytest.raises(MPTAPIError):
        vendor_variant_service.get(created_variant.id)

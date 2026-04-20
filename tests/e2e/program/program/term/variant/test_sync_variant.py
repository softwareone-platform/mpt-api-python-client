import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def vendor_variant_service(mpt_vendor, program_id, term_id):
    return mpt_vendor.program.programs.terms(program_id).variants(term_id)


@pytest.fixture
def created_variant(vendor_variant_service, variant_data_factory, pdf_fd):
    variant_data = variant_data_factory()
    variant = vendor_variant_service.create(variant_data, pdf_fd)
    yield variant
    try:
        vendor_variant_service.delete(variant.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete variant {variant.id}: {error.title}")  # noqa: WPS421


@pytest.fixture
def created_variant_from_url(vendor_variant_service, variant_data_factory, pdf_url):
    variant_data = variant_data_factory(variant_type="Online", asset_url=pdf_url)
    variant = vendor_variant_service.create(variant_data)
    yield variant
    try:
        vendor_variant_service.delete(variant.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete variant {variant.id}: {error.title}")  # noqa: WPS421


def test_create_variant(created_variant, variant_data_factory):
    variant_data = variant_data_factory()

    result = created_variant.name == variant_data["name"]

    assert result is True


def test_create_variant_from_url(created_variant_from_url, variant_data_factory):
    variant_data = variant_data_factory(
        variant_type="Online", asset_url="https://example.com/file.pdf"
    )

    result = created_variant_from_url.name == variant_data["name"]

    assert result is True


def test_update_variant(vendor_variant_service, created_variant):
    update_data = {"name": "E2E Updated Program Term Variant"}

    result = vendor_variant_service.update(created_variant.id, update_data)

    assert result.name == "E2E Updated Program Term Variant"


def test_delete_variant(vendor_variant_service, created_variant):
    variant_data = created_variant

    result = vendor_variant_service.delete(variant_data.id)

    assert result is None


def test_get_variant(vendor_variant_service, variant_id):
    result = vendor_variant_service.get(variant_id)

    assert result.id == variant_id


def test_get_invalid_variant(vendor_variant_service, invalid_variant_id):
    with pytest.raises(MPTAPIError):
        vendor_variant_service.get(invalid_variant_id)


def test_filter_and_select_variants(vendor_variant_service, variant_id):
    select_fields = ["-description", "-audit"]
    filtered_variants = (
        vendor_variant_service
        .filter(RQLQuery(id=variant_id))
        .filter(RQLQuery(name="E2E Seeded Program Terms Variant"))
        .select(*select_fields)
    )

    result = list(filtered_variants.iterate())

    assert len(result) == 1


def test_publish_variant(vendor_variant_service, created_variant):
    result = vendor_variant_service.publish(created_variant.id)

    assert result.status == "Published"


def test_unpublish_variant(vendor_variant_service, created_variant):
    vendor_variant_service.publish(created_variant.id)

    result = vendor_variant_service.unpublish(created_variant.id)

    assert result.status == "Unpublished"

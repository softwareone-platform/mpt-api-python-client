import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def async_vendor_variant_service(async_mpt_vendor, product_id, term_id):
    return async_mpt_vendor.catalog.products.terms(product_id).variants(term_id)


@pytest.fixture
async def async_created_variant(
    variant_data,
    pdf_fd,
    async_vendor_variant_service,
):
    variant = await async_vendor_variant_service.create(variant_data, pdf_fd)
    yield variant
    try:
        await async_vendor_variant_service.delete(variant.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete variant {variant.id}: {error.title}")


@pytest.fixture
async def created_variant_from_url(
    variant_data,
    pdf_url,
    async_vendor_variant_service,
):
    variant_data["type"] = "Online"
    variant_data["assetUrl"] = pdf_url
    variant = await async_vendor_variant_service.create(variant_data)
    yield variant
    try:
        await async_vendor_variant_service.delete(variant.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete variant {variant.id}: {error.title}")


def test_create_variant(async_created_variant):
    variant = async_created_variant
    assert variant.name == "e2e - please delete"


def test_create_variant_from_url(created_variant_from_url, variant_data):
    assert created_variant_from_url.name == variant_data["name"]


async def test_update_variant(
    async_mpt_vendor, product_id, term_id, async_created_variant, async_vendor_variant_service
):
    service = async_vendor_variant_service
    update_data = {"name": "e2e - delete me (updated)"}
    variant = await service.update(async_created_variant.id, update_data)
    assert variant.name == "e2e - delete me (updated)"


async def test_get_variant(
    async_mpt_vendor, product_id, term_id, variant_id, async_vendor_variant_service
):
    service = async_vendor_variant_service
    variant = await service.get(variant_id)
    assert variant.id == variant_id


async def test_get_variant_by_id(
    async_mpt_vendor, product_id, term_id, variant_id, async_vendor_variant_service
):
    service = async_vendor_variant_service
    variant = await service.get(variant_id)
    assert variant.id == variant_id


async def test_iterate_variants(
    async_mpt_vendor, product_id, term_id, async_created_variant, async_vendor_variant_service
):
    service = async_vendor_variant_service
    variants = [variant async for variant in service.iterate()]
    assert any(variant.id == async_created_variant.id for variant in variants)


async def test_filter_variants(
    async_mpt_vendor, product_id, term_id, variant_id, async_vendor_variant_service
):
    select_fields = ["-description"]
    filtered_variants = async_vendor_variant_service.filter(RQLQuery(id=variant_id)).select(
        *select_fields
    )
    variants = [variant async for variant in filtered_variants.iterate()]
    assert len(variants) == 1
    assert variants[0].id == variant_id


async def test_delete_variant(
    async_mpt_vendor, product_id, term_id, async_created_variant, async_vendor_variant_service
):
    service = async_vendor_variant_service
    await service.delete(async_created_variant.id)
    with pytest.raises(MPTAPIError):
        await service.get(async_created_variant.id)

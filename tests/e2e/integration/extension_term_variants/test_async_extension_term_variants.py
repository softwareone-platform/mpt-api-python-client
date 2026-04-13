import pytest

from tests.e2e.helper import assert_async_service_filter_with_iterate

pytestmark = [
    pytest.mark.flaky,
]


def test_create_extension_term_variant(async_created_variant, variant_data):
    result = async_created_variant.name

    assert result == variant_data["name"]


async def test_filter_extension_term_variants(
    async_extension_term_variants_service, async_created_variant
):
    await assert_async_service_filter_with_iterate(
        async_extension_term_variants_service, async_created_variant.id, None
    )  # act


async def test_update_extension_term_variant(
    async_extension_term_variants_service, async_created_variant, short_uuid
):
    update_data = {"name": f"e2e updated {short_uuid}"}

    result = await async_extension_term_variants_service.update(
        async_created_variant.id, update_data
    )

    assert result.name == update_data["name"]


async def test_publish_extension_term_variant(
    async_extension_term_variants_service, async_created_variant
):
    result = await async_extension_term_variants_service.publish(async_created_variant.id)

    assert result.status == "Published"


async def test_unpublish_extension_term_variant(
    async_extension_term_variants_service, async_created_variant
):
    await async_extension_term_variants_service.publish(async_created_variant.id)

    result = await async_extension_term_variants_service.unpublish(async_created_variant.id)

    assert result.status == "Unpublished"


async def test_delete_extension_term_variant(
    async_extension_term_variants_service, async_created_variant
):
    await async_extension_term_variants_service.delete(async_created_variant.id)  # act

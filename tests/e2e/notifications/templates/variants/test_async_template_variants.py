from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from tests.e2e.helper import (
    assert_async_service_filter_with_iterate,
    assert_async_update_resource,
)

pytestmark = [pytest.mark.flaky]


def test_create_template_variant(async_created_template_variant, template_variant_data):
    result = async_created_template_variant.subject

    assert result == template_variant_data["subject"]


async def test_get_template_variant(
    async_template_variants_service, async_created_template_variant
):
    result = await async_template_variants_service.get(async_created_template_variant.id)

    assert result.id == async_created_template_variant.id


async def test_get_template_variant_not_found(async_template_variants_service):
    bogus_id = "NTL-0000-0000-0000"

    with pytest.raises(MPTAPIError) as error:
        await async_template_variants_service.get(bogus_id)

    assert error.value.status_code == HTTPStatus.NOT_FOUND


async def test_update_template_variant(
    async_template_variants_service, async_created_template_variant, short_uuid
):
    new_subject = f"e2e template variant updated {short_uuid}"

    await assert_async_update_resource(  # act
        async_template_variants_service, async_created_template_variant.id, "subject", new_subject
    )


async def test_activate_template_variant(
    async_template_variants_service, async_created_template_variant
):
    result = await async_template_variants_service.activate(async_created_template_variant.id)

    assert result.status == "Active"
    assert result.default


async def test_disable_template_variant(
    async_template_variants_service,
    async_created_template_variant,
    secondary_template_variant_data,
):
    # The default variant cannot be disabled, so the test disables a second active variant.
    await async_template_variants_service.activate(async_created_template_variant.id)
    secondary_variant = await async_template_variants_service.create(
        secondary_template_variant_data
    )
    await async_template_variants_service.activate(secondary_variant.id)

    result = await async_template_variants_service.disable(secondary_variant.id)

    assert result.status == "Disabled"


async def test_delete_template_variant(
    async_template_variants_service, async_created_template_variant
):
    await async_template_variants_service.delete(async_created_template_variant.id)

    result = await async_template_variants_service.get(async_created_template_variant.id)

    assert result.status == "Deleted"


async def test_delete_template_variant_not_found(async_template_variants_service):
    # The platform answers a delete on an unknown id with 400, not 404.
    bogus_id = "NTL-0000-0000-0000"

    with pytest.raises(MPTAPIError) as error:
        await async_template_variants_service.delete(bogus_id)

    assert error.value.status_code == HTTPStatus.BAD_REQUEST


async def test_filter_template_variants(
    async_template_variants_service, async_created_template_variant
):
    await assert_async_service_filter_with_iterate(  # act
        async_template_variants_service, async_created_template_variant.id, None
    )

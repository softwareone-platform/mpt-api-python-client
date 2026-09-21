from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from tests.e2e.helper import (
    assert_async_service_filter_with_iterate,
    assert_async_update_resource,
)

pytestmark = [pytest.mark.flaky]


def test_create_template(async_created_template, template_data):
    result = async_created_template.name

    assert result == template_data["name"]


async def test_get_template(async_templates_service, async_created_template):
    result = await async_templates_service.get(async_created_template.id)

    assert result.id == async_created_template.id


async def test_get_template_not_found(async_templates_service):
    bogus_id = "NTM-0000-0000"

    with pytest.raises(MPTAPIError) as error:
        await async_templates_service.get(bogus_id)

    assert error.value.status_code == HTTPStatus.NOT_FOUND


async def test_update_template(async_templates_service, async_created_template, short_uuid):
    new_description = f"e2e template updated {short_uuid}"

    await assert_async_update_resource(  # act
        async_templates_service, async_created_template.id, "description", new_description
    )


async def test_activate_template(
    async_templates_service,
    async_template_variants_service,
    async_created_template,
    async_created_template_variant,
):
    await async_template_variants_service.activate(async_created_template_variant.id)

    result = await async_templates_service.activate(async_created_template.id)

    assert result.status == "Active"
    assert result.default_variant.id == async_created_template_variant.id


async def test_disable_template(async_templates_service, async_active_template):
    result = await async_templates_service.disable(async_active_template.id)

    assert result.status == "Disabled"


async def test_delete_template(async_templates_service, async_created_template):
    await async_templates_service.delete(async_created_template.id)

    result = await async_templates_service.get(async_created_template.id)

    assert result.status == "Deleted"


async def test_delete_template_not_found(async_templates_service):
    # The platform answers a delete on an unknown id with 400, not 404.
    bogus_id = "NTM-0000-0000"

    with pytest.raises(MPTAPIError) as error:
        await async_templates_service.delete(bogus_id)

    assert error.value.status_code == HTTPStatus.BAD_REQUEST


async def test_filter_templates(async_templates_service, async_created_template):
    await assert_async_service_filter_with_iterate(  # act
        async_templates_service, async_created_template.id, None
    )

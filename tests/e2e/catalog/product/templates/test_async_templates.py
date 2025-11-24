import pytest

from mpt_api_client import RQLQuery
from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def async_template_service(async_mpt_vendor, product_id):
    return async_mpt_vendor.catalog.products.templates(product_id)


@pytest.fixture
async def async_created_template(async_template_service, template_payload):
    template = await async_template_service.create(template_payload)
    yield template
    try:
        await async_template_service.delete(template.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete template {template.id}: {error.title}")


async def test_list_templates(async_template_service):
    templates = [template async for template in async_template_service.iterate()]
    assert isinstance(templates, list)


def test_created_template(async_created_template, template_payload):
    assert async_created_template.name == template_payload["name"]


async def test_get_template(async_template_service, template_id):
    template = await async_template_service.get(template_id)

    assert template.id == template_id


async def test_update_template(async_created_template, async_template_service):
    update_payload = {"name": "Updated name"}
    updated_template = await async_template_service.update(
        async_created_template.id, update_payload
    )
    assert updated_template.name == "Updated name"


async def test_delete_template(async_template_service, async_created_template):
    await async_template_service.delete(async_created_template.id)

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_template_service.get(async_created_template.id)


async def test_filter_templates(async_template_service, template_id):
    template = await async_template_service.filter(RQLQuery(id=template_id)).fetch_one()
    assert template.id == template_id


async def test_not_found(async_template_service):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_template_service.get("TMP-000-000")


async def test_create_wrong_data(async_template_service):
    with pytest.raises(MPTAPIError, match=r"400 One or more validation errors occurred"):
        await async_template_service.create({})

import pytest

from tests.e2e.helper import (
    async_create_fixture_resource_and_delete,
    create_fixture_resource_and_delete,
)

# A template can only be activated once it has a default variant, and the first variant
# activated on a template becomes its default. Deleting a template soft-deletes its variants,
# so the variant fixtures only create and leave the cleanup to the template teardown.


@pytest.fixture
def templates_service(mpt_ops):
    return mpt_ops.notifications.templates


@pytest.fixture
def async_templates_service(async_mpt_ops):
    return async_mpt_ops.notifications.templates


@pytest.fixture
def template_data(short_uuid, category_id):
    return {
        "name": f"e2e template {short_uuid}",
        "description": f"e2e template - please delete {short_uuid}",
        "type": "Manual",
        "category": {"id": category_id},
    }


@pytest.fixture
def template_variant_data(short_uuid):
    return {
        "languageCode": "en-US",
        "subject": f"e2e template variant {short_uuid}",
        "body": f"e2e template variant body {short_uuid}",
    }


@pytest.fixture
def created_template(templates_service, template_data):
    with create_fixture_resource_and_delete(templates_service, template_data) as template:
        yield template


@pytest.fixture
async def async_created_template(async_templates_service, template_data):
    async with async_create_fixture_resource_and_delete(
        async_templates_service, template_data
    ) as template:
        yield template


@pytest.fixture
def template_variants_service(templates_service, created_template):
    return templates_service.variants(created_template.id)


@pytest.fixture
def async_template_variants_service(async_templates_service, async_created_template):
    return async_templates_service.variants(async_created_template.id)


@pytest.fixture
def created_template_variant(template_variants_service, template_variant_data):
    return template_variants_service.create(template_variant_data)


@pytest.fixture
async def async_created_template_variant(async_template_variants_service, template_variant_data):
    return await async_template_variants_service.create(template_variant_data)


@pytest.fixture
def active_template(
    templates_service, template_variants_service, created_template, created_template_variant
):
    template_variants_service.activate(created_template_variant.id)
    return templates_service.activate(created_template.id)


@pytest.fixture
async def async_active_template(
    async_templates_service,
    async_template_variants_service,
    async_created_template,
    async_created_template_variant,
):
    await async_template_variants_service.activate(async_created_template_variant.id)
    return await async_templates_service.activate(async_created_template.id)

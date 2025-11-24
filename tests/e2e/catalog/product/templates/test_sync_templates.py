import pytest

from mpt_api_client import RQLQuery
from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def template_service(mpt_vendor, product_id):
    return mpt_vendor.catalog.products.templates(product_id)


@pytest.fixture
def created_template(template_service, template_payload):
    template = template_service.create(template_payload)

    yield template

    try:
        template_service.delete(template.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete template {template.id}: {error.title}")


def test_list_templates(template_service, product_id):
    templates = list(template_service.iterate())
    assert isinstance(templates, list)


def test_created_template(created_template, template_payload):
    assert created_template.name == template_payload["name"]


def test_get_template(template_service, template_id):
    template = template_service.get(template_id)

    assert template.id == template_id


def test_update_template(created_template, template_service):
    update_payload = {"name": "Updated name"}

    updated_template = template_service.update(created_template.id, update_payload)

    assert updated_template.name == "Updated name"


def test_delete_template(template_service, created_template, template_payload):
    template_service.delete(created_template.id)

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        template_service.get(created_template.id)


def test_filter_templates(template_service, template_id):
    template = template_service.filter(RQLQuery(id=template_id)).fetch_one()

    assert template.id == template_id


def test_not_found(template_service):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        template_service.get("TMP-000-000")


def test_create_wrong_data(template_service):
    with pytest.raises(MPTAPIError, match=r"400 One or more validation errors occurred"):
        template_service.create({})

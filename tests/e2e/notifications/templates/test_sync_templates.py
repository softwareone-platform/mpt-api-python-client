from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from tests.e2e.helper import assert_service_filter_with_iterate, assert_update_resource

pytestmark = [pytest.mark.flaky]


def test_create_template(created_template, template_data):
    result = created_template.name

    assert result == template_data["name"]


def test_get_template(templates_service, created_template):
    result = templates_service.get(created_template.id)

    assert result.id == created_template.id


def test_get_template_not_found(templates_service):
    bogus_id = "NTM-0000-0000"

    with pytest.raises(MPTAPIError) as error:
        templates_service.get(bogus_id)

    assert error.value.status_code == HTTPStatus.NOT_FOUND


def test_update_template(templates_service, created_template, short_uuid):
    new_description = f"e2e template updated {short_uuid}"

    assert_update_resource(  # act
        templates_service, created_template.id, "description", new_description
    )


def test_activate_template(
    templates_service, template_variants_service, created_template, created_template_variant
):
    template_variants_service.activate(created_template_variant.id)

    result = templates_service.activate(created_template.id)

    assert result.status == "Active"
    assert result.default_variant.id == created_template_variant.id


def test_disable_template(templates_service, active_template):
    result = templates_service.disable(active_template.id)

    assert result.status == "Disabled"


def test_delete_template(templates_service, created_template):
    templates_service.delete(created_template.id)

    result = templates_service.get(created_template.id)

    assert result.status == "Deleted"


def test_delete_template_not_found(templates_service):
    # The platform answers a delete on an unknown id with 400, not 404.
    bogus_id = "NTM-0000-0000"

    with pytest.raises(MPTAPIError) as error:
        templates_service.delete(bogus_id)

    assert error.value.status_code == HTTPStatus.BAD_REQUEST


def test_filter_templates(templates_service, created_template):
    assert_service_filter_with_iterate(templates_service, created_template.id, None)  # act

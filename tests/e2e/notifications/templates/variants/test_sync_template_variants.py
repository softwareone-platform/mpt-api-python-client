from http import HTTPStatus

import pytest

from mpt_api_client.exceptions import MPTAPIError
from tests.e2e.helper import assert_service_filter_with_iterate, assert_update_resource

pytestmark = [pytest.mark.flaky]


def test_create_template_variant(created_template_variant, template_variant_data):
    result = created_template_variant.subject

    assert result == template_variant_data["subject"]


def test_get_template_variant(template_variants_service, created_template_variant):
    result = template_variants_service.get(created_template_variant.id)

    assert result.id == created_template_variant.id


def test_get_template_variant_not_found(template_variants_service):
    bogus_id = "NTL-0000-0000-0000"

    with pytest.raises(MPTAPIError) as error:
        template_variants_service.get(bogus_id)

    assert error.value.status_code == HTTPStatus.NOT_FOUND


def test_update_template_variant(template_variants_service, created_template_variant, short_uuid):
    new_subject = f"e2e template variant updated {short_uuid}"

    assert_update_resource(  # act
        template_variants_service, created_template_variant.id, "subject", new_subject
    )


def test_activate_template_variant(template_variants_service, created_template_variant):
    result = template_variants_service.activate(created_template_variant.id)

    assert result.status == "Active"
    assert result.default


def test_disable_template_variant(
    template_variants_service, created_template_variant, secondary_template_variant_data
):
    # The default variant cannot be disabled, so the test disables a second active variant.
    template_variants_service.activate(created_template_variant.id)
    secondary_variant = template_variants_service.create(secondary_template_variant_data)
    template_variants_service.activate(secondary_variant.id)

    result = template_variants_service.disable(secondary_variant.id)

    assert result.status == "Disabled"


def test_delete_template_variant(template_variants_service, created_template_variant):
    template_variants_service.delete(created_template_variant.id)

    result = template_variants_service.get(created_template_variant.id)

    assert result.status == "Deleted"


def test_delete_template_variant_not_found(template_variants_service):
    # The platform answers a delete on an unknown id with 400, not 404.
    bogus_id = "NTL-0000-0000-0000"

    with pytest.raises(MPTAPIError) as error:
        template_variants_service.delete(bogus_id)

    assert error.value.status_code == HTTPStatus.BAD_REQUEST


def test_filter_template_variants(template_variants_service, created_template_variant):
    assert_service_filter_with_iterate(  # act
        template_variants_service, created_template_variant.id, None
    )

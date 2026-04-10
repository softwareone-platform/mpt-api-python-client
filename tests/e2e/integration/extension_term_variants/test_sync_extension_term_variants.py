import pytest

from tests.e2e.helper import assert_service_filter_with_iterate

pytestmark = [
    pytest.mark.flaky,
]


@pytest.mark.skip(reason="creates real resources; run manually only")
def test_create_extension_term_variant(created_variant, variant_data):
    result = created_variant.name

    assert result == variant_data["name"]


def test_filter_extension_term_variants(extension_term_variants_service, term_id):
    assert_service_filter_with_iterate(extension_term_variants_service, term_id, None)  # act


@pytest.mark.skip(reason="modifies real resources; run manually only")
def test_update_extension_term_variant(
    extension_term_variants_service, created_variant, short_uuid
):
    update_data = {"name": f"e2e updated {short_uuid}"}

    result = extension_term_variants_service.update(created_variant.id, update_data)

    assert result.name == update_data["name"]


@pytest.mark.skip(reason="modifies real resources; run manually only")
def test_publish_extension_term_variant(extension_term_variants_service, created_variant):
    result = extension_term_variants_service.publish(created_variant.id)

    assert result.status == "Published"


@pytest.mark.skip(reason="modifies real resources; run manually only")
def test_unpublish_extension_term_variant(extension_term_variants_service, created_variant):
    extension_term_variants_service.publish(created_variant.id)

    result = extension_term_variants_service.unpublish(created_variant.id)

    assert result.status == "Unpublished"


@pytest.mark.skip(reason="deletes real resources; run manually only")
def test_delete_extension_term_variant(extension_term_variants_service, created_variant):
    extension_term_variants_service.delete(created_variant.id)  # act

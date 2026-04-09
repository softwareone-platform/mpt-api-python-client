import pytest

from tests.e2e.helper import assert_service_filter_with_iterate

pytestmark = [
    pytest.mark.flaky,
]


def test_create_extension_term(created_term, term_data):
    result = created_term.name

    assert result == term_data["name"]


def test_filter_extension_terms(extension_terms_service, created_term):
    assert_service_filter_with_iterate(extension_terms_service, created_term.id, None)  # act


def test_update_extension_term(extension_terms_service, created_term, short_uuid):
    update_data = {"name": f"e2e updated {short_uuid}"}

    result = extension_terms_service.update(created_term.id, update_data)

    assert result.name == update_data["name"]


def test_publish_extension_term(extension_terms_service, created_term):
    result = extension_terms_service.publish(created_term.id)

    assert result.status == "Published"


def test_unpublish_extension_term(extension_terms_service, created_term):
    extension_terms_service.publish(created_term.id)

    result = extension_terms_service.unpublish(created_term.id)

    assert result.status == "Unpublished"


def test_delete_extension_term(extension_terms_service, created_term):
    extension_terms_service.delete(created_term.id)  # act

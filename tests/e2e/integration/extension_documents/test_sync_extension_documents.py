import pytest

from tests.e2e.helper import assert_service_filter_with_iterate

pytestmark = [
    pytest.mark.flaky,
]


def test_create_extension_document(created_document, document_data):
    result = created_document.name

    assert result == document_data["name"]


def test_filter_extension_documents(extension_documents_service, created_document):
    assert_service_filter_with_iterate(
        extension_documents_service, created_document.id, None
    )  # act


def test_update_extension_document(extension_documents_service, created_document, short_uuid):
    update_data = {"name": f"e2e updated {short_uuid}"}

    result = extension_documents_service.update(created_document.id, update_data)

    assert result.name == update_data["name"]


def test_publish_extension_document(extension_documents_service, created_document):
    result = extension_documents_service.publish(created_document.id)

    assert result.status == "Published"


def test_unpublish_extension_document(extension_documents_service, created_document):
    extension_documents_service.publish(created_document.id)

    result = extension_documents_service.unpublish(created_document.id)

    assert result.status == "Unpublished"


def test_delete_extension_document(extension_documents_service, created_document):
    extension_documents_service.delete(created_document.id)  # act

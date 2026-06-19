import pytest

from mpt_api_client.exceptions import MPTAPIError
from tests.e2e.helper import (
    assert_service_filter_with_iterate,
    assert_update_resource,
    create_fixture_resource_and_delete,
)

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_document_from_file(vendor_document_service, document_data, pdf_fd):
    document_data["documentType"] = "File"
    with create_fixture_resource_and_delete(
        vendor_document_service, document_data, upload_file=pdf_fd
    ) as document:
        yield document


@pytest.fixture
def created_document_from_url(vendor_document_service, document_data, pdf_url):
    document_data["url"] = pdf_url
    with create_fixture_resource_and_delete(vendor_document_service, document_data) as document:
        yield document


def test_create_document(created_document_from_file, document_data):  # noqa: AAA01
    assert created_document_from_file.name == document_data["name"]
    assert created_document_from_file.description == document_data["description"]


def test_create_document_from_url(created_document_from_url, document_data):  # noqa: AAA01
    assert created_document_from_url.name == document_data["name"]
    assert created_document_from_url.description == document_data["description"]


def test_update_document(vendor_document_service, created_document_from_file):
    assert_update_resource(
        vendor_document_service,
        created_document_from_file.id,
        "name",
        "Updated e2e test document - please delete",
    )  # act


def test_get_document(vendor_document_service, created_document_from_file):
    result = vendor_document_service.get(created_document_from_file.id)

    assert result.id == created_document_from_file.id


def test_download_document(vendor_document_service, created_document_from_file):
    result = vendor_document_service.download(created_document_from_file.id)

    assert result.file_contents is not None
    assert result.filename == "empty.pdf"


def test_iterate_documents(vendor_document_service, created_document_from_file):
    documents = list(vendor_document_service.iterate())

    result = any(doc.id == created_document_from_file.id for doc in documents)

    assert result is True


def test_filter_documents(vendor_document_service, created_document_from_file):
    assert_service_filter_with_iterate(
        vendor_document_service, created_document_from_file.id, None
    )  # act


def test_review_and_publish_document(
    vendor_document_service, mpt_ops, created_document_from_file, created_product
):
    ops_service = mpt_ops.catalog.products.documents(created_product.id)
    document = vendor_document_service.review(created_document_from_file.id)
    assert document.status == "Pending"
    document = ops_service.publish(created_document_from_file.id)
    assert document.status == "Published"

    result = ops_service.unpublish(created_document_from_file.id)

    assert result.status == "Unpublished"


def test_not_found(vendor_document_service):
    with pytest.raises(MPTAPIError):
        vendor_document_service.get("DOC-000-000-000")


def test_delete_document(vendor_document_service, created_document_from_file):
    vendor_document_service.delete(created_document_from_file.id)  # act

    with pytest.raises(MPTAPIError):
        vendor_document_service.get(created_document_from_file.id)

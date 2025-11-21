import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_document_from_file(logger, vendor_document_service, document_data, pdf_fd):
    document_data["documenttype"] = "File"
    document = vendor_document_service.create(document_data, pdf_fd)
    yield document
    try:
        vendor_document_service.delete(document.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete document {document.id}: {error.title}")


@pytest.fixture
def created_document_from_url(logger, vendor_document_service, document_data, pdf_url):
    document_data["url"] = pdf_url
    document = vendor_document_service.create(document_data)
    yield document
    try:
        vendor_document_service.delete(document.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete document {document.id}: {error.title}")


def test_create_document(created_document_from_file, document_data):
    assert created_document_from_file.name == document_data["name"]
    assert created_document_from_file.description == document_data["description"]


def test_create_document_from_url(created_document_from_url, document_data):
    assert created_document_from_url.name == document_data["name"]
    assert created_document_from_url.description == document_data["description"]


def test_update_document(vendor_document_service, created_document_from_file):
    update_data = {"name": "Updated e2e test document - please delete"}
    document = vendor_document_service.update(created_document_from_file.id, update_data)
    assert document.name == update_data["name"]


def test_get_document(vendor_document_service, document_id):
    document = vendor_document_service.get(document_id)
    assert document.id == document_id


def test_download_document(vendor_document_service, document_id):
    file_response = vendor_document_service.download(document_id)
    assert file_response.file_contents is not None
    assert file_response.filename == "pdf - empty.pdf"


def test_iterate_documents(vendor_document_service, created_document_from_file):
    documents = list(vendor_document_service.iterate())
    assert any(doc.id == created_document_from_file.id for doc in documents)


def test_filter_documents(vendor_document_service, created_document_from_file):
    documents = list(
        vendor_document_service.filter(RQLQuery(id=created_document_from_file.id)).iterate()
    )
    assert len(documents) == 1
    assert documents[0].id == created_document_from_file.id


@pytest.mark.skip(reason="Leaves test documents in published state")
def test_review_and_publish_document(mpt_vendor, mpt_ops, created_document_from_file, product_id):
    vendor_service = mpt_vendor.catalog.products.documents(product_id)
    ops_service = mpt_ops.catalog.products.documents(product_id)

    document = vendor_service.review(created_document_from_file.id)
    assert document.status == "Pending"

    document = ops_service.publish(created_document_from_file.id)
    assert document.status == "Published"

    document = ops_service.unpublish(created_document_from_file.id)
    assert document.status == "Unpublished"


def test_not_found(vendor_document_service):
    with pytest.raises(MPTAPIError):
        vendor_document_service.get("DOC-000-000-000")


def test_delete_document(vendor_document_service, created_document_from_file):
    vendor_document_service.delete(created_document_from_file.id)
    with pytest.raises(MPTAPIError):
        vendor_document_service.get(created_document_from_file.id)

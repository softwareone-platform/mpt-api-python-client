import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_document_from_file(vendor_document_service, document_data_factory, pdf_fd):
    document_data = document_data_factory(document_type="File")
    document = vendor_document_service.create(document_data, pdf_fd)
    yield document, document_data
    try:
        vendor_document_service.delete(document.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete document {document.id}: {error.title}")  # noqa: WPS421


@pytest.fixture
def created_document_from_url(vendor_document_service, document_data_factory, pdf_url):
    document_data = document_data_factory(document_type="Online")
    document_data["url"] = pdf_url
    document = vendor_document_service.create(document_data)
    yield document, document_data
    try:
        vendor_document_service.delete(document.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete document {document.id}: {error.title}")  # noqa: WPS421


def test_create_document(created_document_from_file):  # noqa: AAA01
    result, document_data = created_document_from_file
    assert result.name == document_data["name"]
    assert result.description == document_data["description"]


def test_create_document_from_url(created_document_from_url):  # noqa: AAA01
    result, document_data = created_document_from_url
    assert result.name == document_data["name"]
    assert result.description == document_data["description"]


def test_update_document(vendor_document_service, created_document_from_file):
    update_data = {"name": "Updated e2e test document"}
    document, _ = created_document_from_file

    result = vendor_document_service.update(document.id, update_data)

    assert result.name == update_data["name"]


def test_get_document(vendor_document_service, document_id):
    result = vendor_document_service.get(document_id)

    assert result.id == document_id


def test_download_document(vendor_document_service, document_id):
    result = vendor_document_service.download(document_id)

    assert result.file_contents is not None
    assert result.filename == "empty.pdf"


def test_iterate_documents(vendor_document_service, document_id):
    documents = list(vendor_document_service.iterate())

    result = any(doc.id == document_id for doc in documents)

    assert result is True


def test_filter_documents(vendor_document_service, created_document_from_file):
    document, _ = created_document_from_file

    result = list(vendor_document_service.filter(RQLQuery(id=document.id)).iterate())

    assert len(result) == 1
    assert result[0].id == document.id


def test_not_found_document(vendor_document_service, invalid_document_id):
    with pytest.raises(MPTAPIError):
        vendor_document_service.get(invalid_document_id)


def test_publish_document(vendor_document_service, created_document_from_file):
    document, _ = created_document_from_file

    result = vendor_document_service.publish(document.id)

    assert result.status == "Published"


def test_unpublish_document(vendor_document_service, created_document_from_file):
    document, _ = created_document_from_file
    vendor_document_service.publish(document.id)

    result = vendor_document_service.unpublish(document.id)

    assert result.status == "Unpublished"

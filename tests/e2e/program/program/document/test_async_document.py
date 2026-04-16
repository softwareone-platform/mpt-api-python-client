import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def created_document_from_file(async_vendor_document_service, document_data_factory, pdf_fd):
    document_data = document_data_factory(document_type="File")
    document = await async_vendor_document_service.create(document_data, pdf_fd)
    yield document, document_data
    try:
        await async_vendor_document_service.delete(document.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete document {document.id}: {error.title}")  # noqa: WPS421


@pytest.fixture
async def created_document_from_url(async_vendor_document_service, document_data_factory, pdf_url):
    document_data = document_data_factory(document_type="Online")
    document_data["url"] = pdf_url
    document = await async_vendor_document_service.create(document_data)
    yield document, document_data
    try:
        await async_vendor_document_service.delete(document.id)
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


async def test_update_document(async_vendor_document_service, created_document_from_file):
    update_data = {"name": "Updated e2e test document"}
    document, _ = created_document_from_file

    result = await async_vendor_document_service.update(document.id, update_data)

    assert result.name == update_data["name"]


async def test_get_document(async_vendor_document_service, document_id):
    result = await async_vendor_document_service.get(document_id)

    assert result.id == document_id


async def test_download_document(async_vendor_document_service, document_id):
    result = await async_vendor_document_service.download(document_id)

    assert result.file_contents is not None
    assert result.filename == "empty.pdf"


async def test_iterate_documents(async_vendor_document_service, document_id):
    documents = [doc async for doc in async_vendor_document_service.iterate()]

    result = any(doc.id == document_id for doc in documents)

    assert result is True


async def test_filter_documents(async_vendor_document_service, created_document_from_file):
    document, _ = created_document_from_file
    filtered_service = async_vendor_document_service.filter(RQLQuery(id=document.id))

    result = [doc async for doc in filtered_service.iterate()]

    assert len(result) == 1
    assert result[0].id == document.id


async def test_not_found_document(async_vendor_document_service, invalid_document_id):
    with pytest.raises(MPTAPIError):
        await async_vendor_document_service.get(invalid_document_id)


async def test_publish_document(async_vendor_document_service, created_document_from_file):
    document, _ = created_document_from_file
    result = await async_vendor_document_service.publish(document.id)

    assert result.status == "Published"


async def test_unpublish_document(async_vendor_document_service, created_document_from_file):
    document, _ = created_document_from_file
    await async_vendor_document_service.publish(document.id)

    result = await async_vendor_document_service.unpublish(document.id)

    assert result.status == "Unpublished"

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def async_document_service(async_mpt_vendor, product_id):
    return async_mpt_vendor.catalog.products.documents(product_id)


@pytest.fixture
async def created_document_from_file_async(async_document_service, document_data, pdf_fd):
    document_data["documenttype"] = "File"
    document = await async_document_service.create(document_data, file=pdf_fd)
    yield document
    try:
        await async_document_service.delete(document.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete document {document.id}: {error.title}")


@pytest.fixture
async def created_document_from_link_async(async_document_service, document_data, pdf_url):
    document_data["url"] = pdf_url
    document = await async_document_service.create(document_data)
    yield document
    try:
        await async_document_service.delete(document.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete document {document.id}: {error.title}")


def test_create_document_async(created_document_from_file_async, document_data):  # noqa: AAA01
    assert created_document_from_file_async.name == document_data["name"]
    assert created_document_from_file_async.description == document_data["description"]


def test_create_from_link_async(created_document_from_link_async, pdf_url, document_data):  # noqa: AAA01
    assert created_document_from_link_async.name == document_data["name"]
    assert created_document_from_link_async.description == document_data["description"]


async def test_update_document_async(async_document_service, created_document_from_file_async):
    update_data = {"name": "Updated e2e test document - please delete"}

    result = await async_document_service.update(created_document_from_file_async.id, update_data)

    assert result.name == update_data["name"]


async def test_get_document_async(async_document_service, document_id):
    result = await async_document_service.get(document_id)

    assert result.id == document_id


async def test_download_document_async(async_document_service, document_id):
    result = await async_document_service.download(document_id)

    assert result.file_contents is not None
    assert result.filename == "pdf - empty.pdf"


async def test_iterate_documents_async(async_document_service, created_document_from_file_async):
    documents = [doc async for doc in async_document_service.iterate()]

    result = any(doc.id == created_document_from_file_async.id for doc in documents)

    assert result is True


async def test_filter_documents_async(async_document_service, created_document_from_file_async):
    filtered_service = async_document_service.filter(
        RQLQuery(id=created_document_from_file_async.id)
    )
    documents = [doc async for doc in filtered_service.iterate()]
    assert len(documents) == 1
    assert documents[0].id == created_document_from_file_async.id


@pytest.mark.skip(reason="Leaves test documents in published state")
async def test_review_and_publish_document_async(
    async_mpt_vendor, async_mpt_ops, created_document_from_file_async, product_id
):
    vendor_service = async_mpt_vendor.catalog.products.documents(product_id)
    ops_service = async_mpt_ops.catalog.products.documents(product_id)

    document = await vendor_service.review(created_document_from_file_async.id)
    assert document.status == "Pending"

    document = await ops_service.publish(created_document_from_file_async.id)
    assert document.status == "Published"

    document = await ops_service.unpublish(created_document_from_file_async.id)
    assert document.status == "Unpublished"


async def test_not_found_async(async_document_service):
    with pytest.raises(MPTAPIError):
        await async_document_service.get("DOC-000-000-000")


async def test_delete_document_async(async_document_service, created_document_from_file_async):
    await async_document_service.delete(created_document_from_file_async.id)
    with pytest.raises(MPTAPIError):
        await async_document_service.get(created_document_from_file_async.id)

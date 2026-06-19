import pytest

from mpt_api_client.exceptions import MPTAPIError
from tests.e2e.helper import (
    assert_async_service_filter_with_iterate,
    assert_async_update_resource,
    async_create_fixture_resource_and_delete,
)

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def created_document_from_file_async(async_vendor_document_service, document_data, pdf_fd):
    document_data["documentType"] = "File"
    async with async_create_fixture_resource_and_delete(
        async_vendor_document_service, document_data, upload_file=pdf_fd
    ) as document:
        yield document


@pytest.fixture
async def created_document_from_link_async(async_vendor_document_service, document_data, pdf_url):
    document_data["url"] = pdf_url
    async with async_create_fixture_resource_and_delete(
        async_vendor_document_service, document_data
    ) as document:
        yield document


def test_create_document_async(created_document_from_file_async, document_data):  # noqa: AAA01
    assert created_document_from_file_async.name == document_data["name"]
    assert created_document_from_file_async.description == document_data["description"]


def test_create_from_link_async(created_document_from_link_async, pdf_url, document_data):  # noqa: AAA01
    assert created_document_from_link_async.name == document_data["name"]
    assert created_document_from_link_async.description == document_data["description"]


async def test_update_document_async(
    async_vendor_document_service, created_document_from_file_async
):
    await assert_async_update_resource(
        async_vendor_document_service,
        created_document_from_file_async.id,
        "name",
        "Updated e2e test document - please delete",
    )  # act


async def test_get_document_async(async_vendor_document_service, created_document_from_file_async):
    result = await async_vendor_document_service.get(created_document_from_file_async.id)

    assert result.id == created_document_from_file_async.id


async def test_download_document_async(
    async_vendor_document_service, created_document_from_file_async
):
    result = await async_vendor_document_service.download(created_document_from_file_async.id)

    assert result.file_contents is not None
    assert result.filename == "empty.pdf"


async def test_iterate_documents_async(
    async_vendor_document_service, created_document_from_file_async
):
    documents = [doc async for doc in async_vendor_document_service.iterate()]

    result = any(doc.id == created_document_from_file_async.id for doc in documents)

    assert result is True


async def test_filter_documents_async(
    async_vendor_document_service, created_document_from_file_async
):
    await assert_async_service_filter_with_iterate(
        async_vendor_document_service, created_document_from_file_async.id, None
    )  # act


async def test_review_and_publish_document_async(
    async_vendor_document_service,
    async_mpt_ops,
    created_document_from_file_async,
    async_created_product,
):
    ops_service = async_mpt_ops.catalog.products.documents(async_created_product.id)
    document = await async_vendor_document_service.review(created_document_from_file_async.id)
    assert document.status == "Pending"
    document = await ops_service.publish(created_document_from_file_async.id)
    assert document.status == "Published"

    result = await ops_service.unpublish(created_document_from_file_async.id)

    assert result.status == "Unpublished"


async def test_not_found_async(async_vendor_document_service):
    with pytest.raises(MPTAPIError):
        await async_vendor_document_service.get("DOC-000-000-000")


async def test_delete_document_async(
    async_vendor_document_service, created_document_from_file_async
):
    await async_vendor_document_service.delete(created_document_from_file_async.id)
    with pytest.raises(MPTAPIError):
        await async_vendor_document_service.get(created_document_from_file_async.id)

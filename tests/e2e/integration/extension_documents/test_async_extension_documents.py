import pytest

from tests.e2e.helper import assert_async_service_filter_with_iterate

pytestmark = [
    pytest.mark.flaky,
]


def test_create_extension_document(async_created_document, document_data):
    result = async_created_document.name

    assert result == document_data["name"]


async def test_filter_extension_documents(
    async_extension_documents_service, async_created_document
):
    await assert_async_service_filter_with_iterate(
        async_extension_documents_service, async_created_document.id, None
    )  # act


async def test_update_extension_document(
    async_extension_documents_service, async_created_document, short_uuid
):
    update_data = {"name": f"e2e updated {short_uuid}"}

    result = await async_extension_documents_service.update(async_created_document.id, update_data)

    assert result.name == update_data["name"]


async def test_publish_extension_document(
    async_extension_documents_service, async_created_document
):
    result = await async_extension_documents_service.publish(async_created_document.id)

    assert result.status == "Published"


async def test_unpublish_extension_document(
    async_extension_documents_service, async_created_document
):
    await async_extension_documents_service.publish(async_created_document.id)

    result = await async_extension_documents_service.unpublish(async_created_document.id)

    assert result.status == "Unpublished"


async def test_delete_extension_document(async_extension_documents_service, async_created_document):
    await async_extension_documents_service.delete(async_created_document.id)  # act

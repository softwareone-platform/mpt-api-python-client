import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def async_attachment_service(async_mpt_ops, pricing_policy_id):
    return async_mpt_ops.catalog.pricing_policies.attachments(pricing_policy_id)


@pytest.fixture
async def created_attachment_async(async_attachment_service, attachment_data, pdf_fd):
    attachment = await async_attachment_service.create(attachment_data, file=pdf_fd)
    yield attachment
    try:
        await async_attachment_service.delete(attachment.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete attachment {attachment.id}: {error.title}")


def test_create_attachment_async(created_attachment_async, attachment_data):
    result = created_attachment_async

    assert result.name == attachment_data["name"]
    assert result.description == attachment_data["description"]


async def test_update_attachment_async(async_attachment_service, created_attachment_async):
    update_data = {"name": "Updated e2e test attachment - please delete"}

    result = await async_attachment_service.update(created_attachment_async.id, update_data)

    assert result.name == update_data["name"]


async def test_get_attachment_async(async_attachment_service, attachment_id):
    result = await async_attachment_service.get(attachment_id)

    assert result.id == attachment_id


async def test_download_attachment_async(async_attachment_service, attachment_id):
    result = await async_attachment_service.download(attachment_id)

    assert result.file_contents is not None
    assert result.filename == "empty.pdf"


async def test_iterate_attachments_async(async_attachment_service, created_attachment_async):
    result = [att async for att in async_attachment_service.iterate()]

    assert any(att.id == created_attachment_async.id for att in result)


async def test_filter_attachments_async(async_attachment_service, created_attachment_async):
    filtered_service = async_attachment_service.filter(RQLQuery(id=created_attachment_async.id))

    result = [att async for att in filtered_service.iterate()]

    assert len(result) == 1
    assert result[0].id == created_attachment_async.id


async def test_not_found_async(async_attachment_service):
    with pytest.raises(MPTAPIError):
        await async_attachment_service.get("ATT-000-000-000")


async def test_delete_attachment_async(async_attachment_service, created_attachment_async):
    await async_attachment_service.delete(created_attachment_async.id)

    with pytest.raises(MPTAPIError):
        await async_attachment_service.get(created_attachment_async.id)

import pytest

from mpt_api_client.rql.query_builder import RQLQuery


@pytest.mark.skip(reason="Batches can not be deleted")
async def test_create_batch(async_batch_service, batch_data):
    result = await async_batch_service.create(batch_data)

    assert result is not None


async def test_get_batch(async_batch_service, batch_id):
    result = await async_batch_service.get(batch_id, select=["attachments"])

    assert result.id == batch_id


async def test_iterate_and_filter(async_batch_service, batch_id):
    batches = [batch async for batch in async_batch_service.filter(RQLQuery(id=batch_id)).iterate()]

    assert len(batches) == 1
    assert batches[0].id == batch_id


@pytest.mark.skip(reason="Batches can not be deleted")
async def test_create_batch_with_file(async_batch_service, batch_data, logo_fd):
    result = await async_batch_service.create(batch_data, file=logo_fd)

    assert result is not None


async def test_download_attachment(async_batch_service, batch_id, batch_attachment_id):
    result = await async_batch_service.download_attachment(batch_id, batch_attachment_id)

    assert result.filename == "logo.png"


async def test_get_attachment(async_batch_service, batch_id, batch_attachment_id):
    result = await async_batch_service.get_attachment(batch_id, batch_attachment_id)

    assert result.id == batch_attachment_id

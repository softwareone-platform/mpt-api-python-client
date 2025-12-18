import pytest

from mpt_api_client import RQLQuery


@pytest.mark.skip(reason="Batches can not be deleted")
def test_create_batch(batch_service, batch_data):
    result = batch_service.create(batch_data)

    assert result is not None


def test_get_batch(batch_service, batch_id):
    result = batch_service.get(batch_id)

    assert result.id == batch_id


def test_iterate_and_filter(batch_service, batch_id):
    result = list(batch_service.filter(RQLQuery(id=batch_id)).iterate())

    assert len(result) == 1
    assert result[0].id == batch_id


@pytest.mark.skip(reason="Batches can not be deleted")
def test_create_batch_with_file(batch_service, batch_data, logo_fd):
    result = batch_service.create(batch_data, file=logo_fd)

    assert result is not None


@pytest.mark.skip(reason="Batches attachments not implemented")  # noqa: AAA01
def test_download_attachment():
    # TODO - Implement get and download E2E tests for attachment
    raise NotImplementedError

import pytest

from mpt_api_client.resources.notifications.batches import (
    AsyncBatchesService,
    BatchesService,
)


@pytest.fixture
def batches_service(http_client):
    return BatchesService(http_client=http_client)


@pytest.fixture
def async_batches_service(async_http_client):
    return AsyncBatchesService(http_client=async_http_client)


@pytest.mark.parametrize("method", ["get", "create", "iterate", "get_batch_attachment"])
def test_sync_batches_service_methods(batches_service, method):
    result = hasattr(batches_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "iterate", "get_batch_attachment"])
def test_async_batches_service_methods(async_batches_service, method):
    result = hasattr(async_batches_service, method)

    assert result is True

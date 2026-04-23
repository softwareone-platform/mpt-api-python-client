import pytest

from mpt_api_client.http.async_service import AsyncService
from mpt_api_client.http.service import Service
from mpt_api_client.resources.program.mixins.attachment_mixin import (
    AsyncAttachmentMixin,
    AttachmentMixin,
)
from tests.unit.conftest import DummyModel


class DummyAttachmentService(
    AttachmentMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/dummy/attachments"
    _model_class = DummyModel
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "attachment"


class DummyAsyncAttachmentService(
    AsyncAttachmentMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/dummy/attachments"
    _model_class = DummyModel
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "attachment"


@pytest.fixture
def attachment_service(http_client):
    return DummyAttachmentService(http_client=http_client)


@pytest.fixture
def async_attachment_service(async_http_client):
    return DummyAsyncAttachmentService(http_client=async_http_client)


@pytest.mark.parametrize("method", ["create", "update", "delete", "download", "get"])
def test_mixins_present(attachment_service, method):
    result = hasattr(attachment_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["create", "update", "delete", "download", "get"])
def test_async_mixins_present(async_attachment_service, method):
    result = hasattr(async_attachment_service, method)

    assert result is True

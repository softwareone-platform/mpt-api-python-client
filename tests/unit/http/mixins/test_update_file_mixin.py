import io

import httpx
import pytest
import respx

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import AsyncUpdateFileMixin, UpdateFileMixin
from tests.unit.conftest import DummyModel


class DummyUpdateFileService(
    UpdateFileMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/dummy/update-file"
    _model_class = DummyModel
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "document"


class DummyAsyncUpdateFileService(
    AsyncUpdateFileMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/dummy/update-file"
    _model_class = DummyModel
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "document"


@pytest.fixture
def update_file_service(http_client) -> DummyUpdateFileService:
    return DummyUpdateFileService(http_client=http_client)


@pytest.fixture
def async_update_file_service(async_http_client) -> DummyAsyncUpdateFileService:
    return DummyAsyncUpdateFileService(http_client=async_http_client)


def test_sync_update_file(update_file_service: DummyUpdateFileService) -> None:
    resource_id = "ICON-1234"
    response_expected_data = {"id": resource_id, "name": "Updated Icon Object"}
    file_tuple = ("icon.png", io.BytesIO(b"PNG DATA"), "image/png")
    resource_data = {"name": "Updated Icon Object"}
    with respx.mock:
        mock_route = respx.put(
            f"https://api.example.com/public/v1/dummy/update-file/{resource_id}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=response_expected_data,
            )
        )

        result = update_file_service.update(resource_id, resource_data, file=file_tuple)

    request = mock_route.calls[0].request
    assert mock_route.call_count == 1
    assert (
        b'Content-Disposition: form-data; name="file"; filename="icon.png"\r\n'
        b"Content-Type: image/png\r\n\r\n"
        b"PNG DATA\r\n" in request.content
    )
    assert "multipart/form-data" in request.headers["Content-Type"]
    assert result.to_dict() == response_expected_data
    assert isinstance(result, DummyModel)


def test_update_file_no_file(update_file_service: DummyUpdateFileService) -> None:
    resource_id = "ICON-1234"
    response_expected_data = {"id": resource_id, "name": "Updated Icon Object"}
    resource_data = {"name": "Updated Icon Object"}
    with respx.mock:
        mock_route = respx.put(
            f"https://api.example.com/public/v1/dummy/update-file/{resource_id}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=response_expected_data,
            )
        )

        result = update_file_service.update(resource_id, resource_data)

    request = mock_route.calls[0].request
    assert mock_route.call_count == 1
    assert b'Content-Disposition: form-data; name="file"' not in request.content
    assert "multipart/form-data" in request.headers["Content-Type"]
    assert result.to_dict() == response_expected_data
    assert isinstance(result, DummyModel)


async def test_async_update_file(async_update_file_service: DummyAsyncUpdateFileService) -> None:
    resource_id = "ICON-1234"
    response_expected_data = {"id": resource_id, "name": "Updated Icon Object"}
    file_tuple = ("icon.png", io.BytesIO(b"PNG DATA"), "image/png")
    resource_data = {"name": "Updated Icon Object"}

    with respx.mock:
        mock_route = respx.put(
            f"https://api.example.com/public/v1/dummy/update-file/{resource_id}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=response_expected_data,
            )
        )
        # Act
        result = await async_update_file_service.update(resource_id, resource_data, file=file_tuple)
    assert mock_route.call_count == 1
    request = mock_route.calls[0].request

    assert (
        b'Content-Disposition: form-data; name="file"; filename="icon.png"\r\n'
        b"Content-Type: image/png\r\n\r\n"
        b"PNG DATA\r\n" in request.content
    )
    assert "multipart/form-data" in request.headers["Content-Type"]
    assert result.to_dict() == response_expected_data
    assert isinstance(result, DummyModel)


async def test_async_update_file_no_file(
    async_update_file_service: DummyAsyncUpdateFileService,
) -> None:
    resource_id = "ICON-1234"
    response_expected_data = {"id": resource_id, "name": "Updated Icon Object"}
    resource_data = {"name": "Updated Icon Object"}

    with respx.mock:
        mock_route = respx.put(
            f"https://api.example.com/public/v1/dummy/update-file/{resource_id}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=response_expected_data,
            )
        )
        # Act
        result = await async_update_file_service.update(resource_id, resource_data)
    assert mock_route.call_count == 1
    request = mock_route.calls[0].request

    assert b'Content-Disposition: form-data; name="file"' not in request.content
    assert "multipart/form-data" in request.headers["Content-Type"]
    assert result.to_dict() == response_expected_data
    assert isinstance(result, DummyModel)

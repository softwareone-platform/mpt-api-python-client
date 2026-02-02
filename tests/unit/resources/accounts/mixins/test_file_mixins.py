import httpx
import pytest
import respx

from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (
    AsyncCreateFileMixin,
    AsyncUpdateFileMixin,
    CreateFileMixin,
    UpdateFileMixin,
)
from tests.unit.conftest import DummyModel


class DummyCreateFileService(
    CreateFileMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/dummy/create-file/"
    _model_class = DummyModel
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "resource"


class AsyncDummyCreateFileService(
    AsyncCreateFileMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/dummy/create-file/"
    _model_class = DummyModel
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "resource"


class DummyUpdateFileService(
    UpdateFileMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/dummy/update-file/"
    _model_class = DummyModel
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "resource"


class DummyAsyncUpdateFileService(
    AsyncUpdateFileMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/dummy/update-file/"
    _model_class = DummyModel
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "resource"


@pytest.fixture
def create_file_service(http_client):
    return DummyCreateFileService(http_client=http_client)


@pytest.fixture
def async_create_file_service(async_http_client):
    return AsyncDummyCreateFileService(http_client=async_http_client)


@pytest.fixture
def update_file_service(http_client):
    return DummyUpdateFileService(http_client=http_client)


@pytest.fixture
def async_update_file_service(async_http_client):
    return DummyAsyncUpdateFileService(http_client=async_http_client)


def test_create_file_service(create_file_service, tmp_path):
    resource_data = {"name": "Test File"}
    response_expected_data = {"id": "OBJ-0000-0001", **resource_data}
    with respx.mock:
        mock_route = respx.post("https://api.example.com/public/v1/dummy/create-file/").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        file_path = tmp_path / "file.png"
        file_path.write_bytes(b"fake-file-data")

        with file_path.open("rb") as file_file:
            result = create_file_service.create(resource_data, file_file)

        assert mock_route.call_count == 1
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


def test_create_file_service_no_file(create_file_service):
    resource_data = {"name": "Test File"}
    response_expected_data = {"id": "OBJ-0000-0001", **resource_data}
    with respx.mock:
        mock_route = respx.post("https://api.example.com/public/v1/dummy/create-file/").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = create_file_service.create(resource_data, None)

        assert mock_route.call_count == 1
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


async def test_async_create_file_service(async_create_file_service, tmp_path):
    resource_data = {"name": "Test File"}
    response_expected_data = {"id": "OBJ-0000-0001", **resource_data}
    with respx.mock:
        mock_route = respx.post("https://api.example.com/public/v1/dummy/create-file/").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        file_path = tmp_path / "file.png"
        file_path.write_bytes(b"fake-file-data")

        with file_path.open("rb") as file_file:
            result = await async_create_file_service.create(resource_data, file_file)

        assert mock_route.call_count == 1
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


async def test_async_create_file_service_no_file(async_create_file_service):
    resource_data = {"name": "Test File"}
    response_expected_data = {"id": "OBJ-0000-0001", **resource_data}
    with respx.mock:
        mock_route = respx.post("https://api.example.com/public/v1/dummy/create-file/").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        result = await async_create_file_service.create(resource_data, None)

        assert mock_route.call_count == 1
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


def test_update_file_service(update_file_service, tmp_path):
    resource_data = {"name": "Test File"}
    response_expected_data = {"id": "OBJ-0000-0001", **resource_data}
    with respx.mock:
        mock_route = respx.put(
            "https://api.example.com/public/v1/dummy/update-file/OBJ-0000-0001"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        update_file_path = tmp_path / "file.png"
        update_file_path.write_bytes(b"updated file content")

        with update_file_path.open("rb") as update_file:
            result = update_file_service.update("OBJ-0000-0001", resource_data, update_file)

        assert mock_route.call_count == 1
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


def test_update_file_service_no_file(update_file_service):
    resource_data = {"name": "Test File"}
    response_expected_data = {"id": "OBJ-0000-0001", **resource_data}
    with respx.mock:
        mock_route = respx.put(
            "https://api.example.com/public/v1/dummy/update-file/OBJ-0000-0001"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = update_file_service.update("OBJ-0000-0001", resource_data, None)

        assert mock_route.call_count == 1
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


async def test_async_update_file_service(async_update_file_service, tmp_path):
    resource_data = {"name": "Test File"}
    response_expected_data = {"id": "OBJ-0000-0001", **resource_data}
    with respx.mock:
        mock_route = respx.put(
            "https://api.example.com/public/v1/dummy/update-file/OBJ-0000-0001"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        update_file_path = tmp_path / "file.png"
        update_file_path.write_bytes(b"updated file content")

        with update_file_path.open("rb") as update_file:
            result = await async_update_file_service.update(
                "OBJ-0000-0001", resource_data, update_file
            )

        assert mock_route.call_count == 1
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


async def test_async_update_file_service_no_file(async_update_file_service):
    resource_data = {"name": "Test File"}
    response_expected_data = {"id": "OBJ-0000-0001", **resource_data}
    with respx.mock:
        mock_route = respx.put(
            "https://api.example.com/public/v1/dummy/update-file/OBJ-0000-0001"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await async_update_file_service.update("OBJ-0000-0001", resource_data, None)

        assert mock_route.call_count == 1
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)

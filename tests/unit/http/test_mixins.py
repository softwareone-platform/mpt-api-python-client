import io
import json

import httpx
import pytest
import respx

from mpt_api_client import RQLQuery
from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.http import AsyncService, Service
from mpt_api_client.http.mixins import (  # noqa: WPS235
    AsyncDisableMixin,
    AsyncEnableMixin,
    AsyncFilesOperationsMixin,
    AsyncManagedResourceMixin,
    AsyncModifiableResourceMixin,
    AsyncUpdateFileMixin,
    DisableMixin,
    EnableMixin,
    FilesOperationsMixin,
    ManagedResourceMixin,
    ModifiableResourceMixin,
    UpdateFileMixin,
)
from mpt_api_client.resources.catalog.products_media import (
    AsyncMediaService,
    MediaService,
)
from tests.unit.conftest import DummyModel


class DummyFileOperationsService(
    FilesOperationsMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/dummy/file-ops/"
    _model_class = DummyModel
    _collection_key = "data"


class DummyAsyncFileOperationsService(
    AsyncFilesOperationsMixin[DummyModel],
    AsyncService[DummyModel],
):
    """Dummy asynchronous file operations service for testing."""

    _endpoint = "/public/v1/dummy/file-ops/"
    _model_class = DummyModel
    _collection_key = "data"


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


class EnableDisableService(
    EnableMixin[DummyModel],
    DisableMixin[DummyModel],
    Service[DummyModel],
):
    _endpoint = "/public/v1/dummy/enablable/"
    _model_class = DummyModel


class AsyncEnableDisableService(
    AsyncEnableMixin[DummyModel],
    AsyncDisableMixin[DummyModel],
    AsyncService[DummyModel],
):
    _endpoint = "/public/v1/dummy/enablable/"
    _model_class = DummyModel


@pytest.fixture
def dummy_file_operations_service(http_client):
    """Fixture for DummyFileOperationsService."""
    return DummyFileOperationsService(http_client=http_client)


@pytest.fixture
def async_dummy_file_operations_service(async_http_client):
    """Fixture for DummyAsyncFileOperationsService."""
    return DummyAsyncFileOperationsService(http_client=async_http_client)


@pytest.fixture
def media_service(http_client):
    """Fixture for MediaService."""
    return MediaService(http_client=http_client, endpoint_params={"product_id": "PRD-001"})


@pytest.fixture
def async_media_service(async_http_client):
    """Fixture for AsyncMediaService."""
    return AsyncMediaService(
        http_client=async_http_client, endpoint_params={"product_id": "PRD-001"}
    )


@pytest.fixture
def update_file_service(http_client):
    return DummyUpdateFileService(http_client=http_client)


@pytest.fixture
def async_update_file_service(async_http_client):
    return DummyAsyncUpdateFileService(http_client=async_http_client)


async def test_async_create_mixin(async_dummy_service):
    """Test creating a resource asynchronously."""
    resource_data = {"name": "Test Resource", "status": "active"}
    new_resource_data = {"id": "new-resource-id", "name": "Test Resource", "status": "active"}
    create_response = httpx.Response(httpx.codes.OK, json=new_resource_data)
    with respx.mock:
        mock_route = respx.post("https://api.example.com/api/v1/test").mock(
            return_value=create_response
        )

        result = await async_dummy_service.create(resource_data)

    assert result.to_dict() == new_resource_data
    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.method == "POST"
    assert request.url == "https://api.example.com/api/v1/test"
    assert json.loads(request.content.decode()) == resource_data


async def test_async_delete_mixin(async_dummy_service):
    """Test deleting a resource asynchronously."""
    delete_response = httpx.Response(httpx.codes.NO_CONTENT, json=None)
    with respx.mock:
        mock_route = respx.delete("https://api.example.com/api/v1/test/RES-123").mock(
            return_value=delete_response
        )

        await async_dummy_service.delete("RES-123")  # act

    assert mock_route.call_count == 1


async def test_async_update_resource(async_dummy_service):
    """Test updating a resource asynchronously."""
    resource_data = {"name": "Test Resource", "status": "active"}
    update_response = httpx.Response(httpx.codes.OK, json=resource_data)
    with respx.mock:
        mock_route = respx.put("https://api.example.com/api/v1/test/RES-123").mock(
            return_value=update_response
        )

        await async_dummy_service.update("RES-123", resource_data)  # act

    request = mock_route.calls[0].request
    assert mock_route.call_count == 1
    assert json.loads(request.content.decode()) == resource_data


def test_sync_create_mixin(dummy_service):
    """Test creating a resource synchronously."""
    resource_data = {"name": "Test Resource", "status": "active"}
    new_resource_data = {"id": "new-resource-id", "name": "Test Resource", "status": "active"}
    create_response = httpx.Response(httpx.codes.OK, json=new_resource_data)
    with respx.mock:
        mock_route = respx.post("https://api.example.com/api/v1/test").mock(
            return_value=create_response
        )

        result = dummy_service.create(resource_data)

    assert result.to_dict() == new_resource_data
    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.method == "POST"
    assert request.url == "https://api.example.com/api/v1/test"
    assert json.loads(request.content.decode()) == resource_data


def test_sync_delete_mixin(dummy_service):
    """Test deleting a resource synchronously."""
    delete_response = httpx.Response(httpx.codes.NO_CONTENT, json=None)
    with respx.mock:
        mock_route = respx.delete("https://api.example.com/api/v1/test/RES-123").mock(
            return_value=delete_response
        )

        dummy_service.delete("RES-123")  # act

    assert mock_route.call_count == 1


def test_sync_update_resource(dummy_service):
    """Test updating a resource synchronously."""
    resource_data = {"name": "Test Resource", "status": "active"}
    update_response = httpx.Response(httpx.codes.OK, json=resource_data)
    with respx.mock:
        mock_route = respx.put("https://api.example.com/api/v1/test/RES-123").mock(
            return_value=update_response
        )

        dummy_service.update("RES-123", resource_data)  # act

    request = mock_route.calls[0].request
    assert mock_route.call_count == 1
    assert json.loads(request.content.decode()) == resource_data


async def test_async_file_create_with_data(async_media_service):
    """Test creating a file resource asynchronously with additional data."""
    media_data = {"id": "MED-133"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=media_data,
            )
        )
        media_image = ("test.jpg", io.BytesIO(b"Image content"), "image/jpeg")

        result = await async_media_service.create({"name": "Product image"}, file=media_image)

    request = mock_route.calls[0].request
    assert (
        b'Content-Disposition: form-data; name="media"\r\n'
        b"Content-Type: application/json\r\n\r\n"
        b'{"name":"Product image"}\r\n' in request.content
    )
    assert (
        b'Content-Disposition: form-data; name="file"; filename="test.jpg"\r\n'
        b"Content-Type: image/jpeg\r\n\r\n"
        b"Image content\r\n" in request.content
    )
    assert "multipart/form-data" in request.headers["Content-Type"]
    assert result.to_dict() == media_data


async def test_async_file_create_no_data(async_media_service):
    """Test creating a file resource asynchronously without additional data."""
    media_data = {"id": "MED-133"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=media_data,
            )
        )
        new_media = await async_media_service.create(
            {}, file=("test.jpg", io.BytesIO(b"Image content"), "image/jpeg")
        )

    request = mock_route.calls[0].request

    assert (
        b'Content-Disposition: form-data; name="file"; filename="test.jpg"\r\n'
        b"Content-Type: image/jpeg\r\n\r\n"
        b"Image content\r\n" in request.content
    )
    assert new_media.to_dict() == media_data


async def test_async_file_download_request_and_headers(async_media_service):
    """Test request/response and headers for async file download."""
    media_content = b"Image file content or binary data"
    with respx.mock:
        mock_resource = respx.get(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media/MED-456",
            headers={"Accept": "application/json"},
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json={"id": "MED-456", "name": "Product image", "content_type": "image/jpg"},
            )
        )
        mock_download = respx.get(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media/MED-456",
            headers={"Accept": "image/jpg"},
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={
                    "content-type": "image/jpg",
                    "content-disposition": 'form-data; name="file"; filename="product_image.jpg"',
                },
                content=media_content,
            )
        )
        # Act
        await async_media_service.download("MED-456")

    assert mock_resource.call_count == 1
    request = mock_download.calls[0].request
    accept_header = (b"Accept", b"image/jpg")
    assert accept_header in request.headers.raw
    assert mock_download.call_count == 1


async def test_async_file_download_content_and_metadata(async_media_service):
    """Test file content and metadata for async file download."""
    media_content = b"Image file content or binary data"
    with respx.mock:
        respx.get(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media/MED-456",
            headers={"Accept": "application/json"},
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json={"id": "MED-456", "name": "Product image", "content_type": "image/jpg"},
            )
        )
        respx.get(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media/MED-456",
            headers={"Accept": "image/jpg"},
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={
                    "content-type": "image/jpg",
                    "content-disposition": 'form-data; name="file"; filename="product_image.jpg"',
                },
                content=media_content,
            )
        )
        result = await async_media_service.download("MED-456")

    assert result.file_contents == media_content
    assert result.content_type == "image/jpg"
    assert result.filename == "product_image.jpg"


def test_sync_file_download_request_and_headers(media_service):
    """Test request/response and headers for sync file download."""
    media_content = b"Image file content or binary data"
    with respx.mock:
        mock_resource = respx.get(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media/MED-456",
            headers={"Accept": "application/json"},
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json={"id": "MED-456", "name": "Product image", "content_type": "image/jpg"},
            )
        )
        mock_download = respx.get(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media/MED-456",
            headers={"Accept": "image/jpg"},
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={
                    "content-type": "image/jpg",
                    "content-disposition": 'form-data; name="file"; filename="product_image.jpg"',
                },
                content=media_content,
            )
        )
        media_service.download("MED-456")
    assert mock_resource.call_count == 1

    result = mock_download.calls[0].request

    # Assert
    accept_header = (b"Accept", b"image/jpg")
    assert accept_header in result.headers.raw
    assert mock_download.call_count == 1


def test_sync_file_download_content_and_metadata(media_service):
    """Test file content and metadata for sync file download."""
    media_content = b"Image file content or binary data"
    with respx.mock:
        respx.get(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media/MED-456",
            headers={"Accept": "application/json"},
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json={"id": "MED-456", "name": "Product image", "content_type": "image/jpg"},
            )
        )
        respx.get(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media/MED-456",
            headers={"Accept": "image/jpg"},
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={
                    "content-type": "image/jpg",
                    "content-disposition": 'form-data; name="file"; filename="product_image.jpg"',
                },
                content=media_content,
            )
        )

        result = media_service.download("MED-456")

    assert result.file_contents == media_content
    assert result.content_type == "image/jpg"
    assert result.filename == "product_image.jpg"


def test_sync_file_create_with_data(media_service):
    """Test creating a file resource synchronously with additional data."""
    media_data = {"id": "MED-133"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=media_data,
            )
        )
        image_file = ("test.jpg", io.BytesIO(b"Image content"), "image/jpeg")

        result = media_service.create({"name": "Product image"}, image_file)

    request = mock_route.calls[0].request
    assert (
        b'Content-Disposition: form-data; name="media"\r\n'
        b"Content-Type: application/json\r\n\r\n"
        b'{"name":"Product image"}\r\n' in request.content
    )
    assert (
        b'Content-Disposition: form-data; name="file"; filename="test.jpg"\r\n'
        b"Content-Type: image/jpeg\r\n\r\n"
        b"Image content\r\n" in request.content
    )
    assert "multipart/form-data" in request.headers["Content-Type"]
    assert result.to_dict() == media_data


def test_sync_file_create_no_data(media_service):
    """Test creating a file resource synchronously without additional data."""
    media_data = {"id": "MED-133"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=media_data,
            )
        )
        image_file = ("test.jpg", io.BytesIO(b"Image content"), "image/jpeg")

        result = media_service.create({}, image_file)

    request = mock_route.calls[0].request
    assert (
        b'Content-Disposition: form-data; name="file"; filename="test.jpg"\r\n'
        b"Content-Type: image/jpeg\r\n\r\n"
        b"Image content\r\n" in request.content
    )
    assert result.to_dict() == media_data


@pytest.mark.parametrize(
    "select_value",
    [
        ["id", "name"],
        "id,name",
    ],
)
def test_sync_get_mixin(dummy_service, select_value):
    """Test getting a resource synchronously with different select parameter formats."""
    resource_data = {"id": "RES-123", "name": "Test Resource"}
    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/api/v1/test/RES-123", params={"select": "id,name"}
        ).mock(return_value=httpx.Response(httpx.codes.OK, json=resource_data))

        result = dummy_service.get("RES-123", select=select_value)

    request = mock_route.calls[0].request
    accept_header = (b"Accept", b"application/json")
    assert accept_header in request.headers.raw
    assert result.to_dict() == resource_data


async def test_async_get(async_dummy_service):
    """Test getting a resource asynchronously with a list select parameter."""
    resource_data = {"id": "RES-123", "name": "Test Resource"}
    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/api/v1/test/RES-123", params={"select": "id,name"}
        ).mock(return_value=httpx.Response(httpx.codes.OK, json=resource_data))

        result = await async_dummy_service.get("RES-123", select=["id", "name"])

    request = mock_route.calls[0].request
    accept_header = (b"Accept", b"application/json")
    assert accept_header in request.headers.raw
    assert result.to_dict() == resource_data


async def test_async_get_select_str(async_dummy_service):
    """Test getting a resource asynchronously with a string select parameter."""
    resource_data = {"id": "RES-123", "name": "Test Resource"}
    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/api/v1/test/RES-123", params={"select": "id,name"}
        ).mock(return_value=httpx.Response(httpx.codes.OK, json=resource_data))

        result = await async_dummy_service.get("RES-123", select="id,name")

    request = mock_route.calls[0].request
    accept_header = (b"Accept", b"application/json")
    assert accept_header in request.headers.raw
    assert result.to_dict() == resource_data


def test_queryable_mixin_order_by(dummy_service):
    result = dummy_service.order_by("created", "-name")

    assert result != dummy_service
    assert dummy_service.query_state.order_by is None
    assert result.query_state.order_by == ["created", "-name"]
    assert result.http_client is dummy_service.http_client
    assert result.endpoint_params == dummy_service.endpoint_params


def test_queryable_mixin_order_by_exception(dummy_service):
    """Test that setting order_by multiple times raises an exception."""
    ordered_service = dummy_service.order_by("created")

    with pytest.raises(
        ValueError, match=r"Ordering is already set. Cannot set ordering multiple times."
    ):
        ordered_service.order_by("name")


def test_queryable_mixin_filter(dummy_service, filter_status_active):
    result = dummy_service.filter(filter_status_active)

    assert result != dummy_service
    assert dummy_service.query_state.filter is None
    assert result.query_state.filter == filter_status_active
    assert result.http_client is dummy_service.http_client
    assert result.endpoint_params == dummy_service.endpoint_params


def test_queryable_mixin_filters(dummy_service):
    """Test applying multiple filters to a queryable service."""
    filter1 = RQLQuery(status="active")
    filter2 = RQLQuery(name="test")

    result = dummy_service.filter(filter1).filter(filter2)

    assert dummy_service.query_state.filter is None
    assert result.query_state.filter == filter1 & filter2


def test_queryable_mixin_select(dummy_service):
    result = dummy_service.select("id", "name", "-audit")

    assert result != dummy_service
    assert dummy_service.query_state.select is None
    assert result.query_state.select == ["id", "name", "-audit"]
    assert result.http_client is dummy_service.http_client
    assert result.endpoint_params == dummy_service.endpoint_params


def test_queryable_mixin_select_exception(dummy_service):
    """Test that setting select fields multiple times raises an exception."""
    selected_service = dummy_service.select("id", "name")

    with pytest.raises(
        ValueError, match=r"Select fields are already set. Cannot set select fields multiple times."
    ):
        selected_service.select("other_field")


def test_queryable_mixin_method_chaining(dummy_service, filter_status_active):
    result = (
        dummy_service.filter(filter_status_active).order_by("created", "-name").select("id", "name")
    )

    assert result != dummy_service
    assert result.query_state.filter == filter_status_active
    assert result.query_state.order_by == ["created", "-name"]
    assert result.query_state.select == ["id", "name"]


def test_col_mx_fetch_one_success(dummy_service, single_result_response):
    """Test fetching a single resource successfully."""
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=single_result_response
        )

        result = dummy_service.fetch_one()

    assert result.id == "ID-1"
    assert result.name == "Test Resource"
    assert mock_route.called
    first_request = mock_route.calls[0].request
    assert "limit=1" in str(first_request.url)
    assert "offset=0" in str(first_request.url)


def test_col_mx_fetch_one_no_results(dummy_service, no_results_response):
    """Test fetching a single resource when no results are returned."""
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test").mock(return_value=no_results_response)

        with pytest.raises(ValueError, match="Expected one result, but got zero results"):
            dummy_service.fetch_one()


def test_col_mx_fetch_one_multiple_results(dummy_service, multiple_results_response):
    """Test fetching a single resource when multiple results are returned."""
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test").mock(
            return_value=multiple_results_response
        )

        with pytest.raises(ValueError, match=r"Expected one result, but got 2 results"):
            dummy_service.fetch_one()


def test_col_mx_fetch_one_with_filters(dummy_service, single_result_response, filter_status_active):
    """Test fetching a single resource with filters applied."""
    filtered_collection = (
        dummy_service.filter(filter_status_active).select("id", "name").order_by("created")
    )
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=single_result_response
        )

        result = filtered_collection.fetch_one()

    assert result.id == "ID-1"
    assert mock_route.called
    first_request = mock_route.calls[0].request
    assert first_request.method == "GET"
    assert first_request.url == (
        "https://api.example.com/api/v1/test"
        "?limit=1&offset=0&order=created"
        "&select=id,name&eq(status,active)"
    )


def test_col_mx_fetch_page_with_filter(dummy_service, list_response, filter_status_active):
    """Test fetching a page of resources with filters applied."""
    custom_collection = (
        dummy_service
        .filter(filter_status_active)
        .select("-audit", "product.agreements", "-product.agreements.product")
        .order_by("-created", "name")
    )
    expected_url = (
        "https://api.example.com/api/v1/test?limit=10&offset=5"
        "&order=-created,name"
        "&select=-audit,product.agreements,-product.agreements.product"
        "&eq(status,active)"
    )
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=list_response
        )

        result = custom_collection.fetch_page(limit=10, offset=5)

    assert result.to_list() == [{"id": "ID-1"}]
    assert mock_route.called
    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.method == "GET"
    assert request.url == expected_url


def test_col_mx_iterate_single_page(dummy_service, single_page_response):
    """Test iterating over a single page of resources."""
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=single_page_response
        )

        result = list(dummy_service.iterate())

    request = mock_route.calls[0].request
    assert len(result) == 2
    assert result[0].to_dict() == {"id": "ID-1", "name": "Resource 1"}
    assert result[1].to_dict() == {"id": "ID-2", "name": "Resource 2"}
    assert mock_route.call_count == 1
    assert request.url == "https://api.example.com/api/v1/test?limit=100&offset=0"


def test_col_mx_iterate_multiple_pages(
    dummy_service, multi_page_response_page1, multi_page_response_page2
):
    """Test iterating over multiple pages of resources."""
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test", params={"limit": 2, "offset": 0}).mock(
            return_value=multi_page_response_page1
        )
        respx.get("https://api.example.com/api/v1/test", params={"limit": 2, "offset": 2}).mock(
            return_value=multi_page_response_page2
        )

        result = list(dummy_service.iterate(2))

    assert len(result) == 4
    assert result[0].id == "ID-1"
    assert result[1].id == "ID-2"
    assert result[2].id == "ID-3"
    assert result[3].id == "ID-4"


def test_col_mx_iterate_empty_results(dummy_service, empty_response):
    """Test iterating over an empty set of resources."""
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=empty_response
        )

        result = list(dummy_service.iterate(2))

    assert len(result) == 0
    assert mock_route.call_count == 1


def test_col_mx_iterate_no_meta(dummy_service, no_meta_response):
    """Test iterating over resources when no metadata is provided."""
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=no_meta_response
        )

        result = list(dummy_service.iterate())

    assert len(result) == 2
    assert result[0].id == "ID-1"
    assert result[1].id == "ID-2"
    assert mock_route.call_count == 1


def test_col_mx_iterate_with_filters(dummy_service, filter_status_active):
    """Test iterating over resources with filters applied."""
    filtered_collection = (
        dummy_service.filter(filter_status_active).select("id", "name").order_by("created")
    )
    response = httpx.Response(
        httpx.codes.OK,
        json={
            "data": [{"id": "ID-1", "name": "Active Resource"}],
            "$meta": {
                "pagination": {
                    "total": 1,
                    "offset": 0,
                    "limit": 100,
                }
            },
        },
    )
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(return_value=response)

        result = list(filtered_collection.iterate())

    assert len(result) == 1
    assert result[0].id == "ID-1"
    assert result[0].name == "Active Resource"
    request = mock_route.calls[0].request
    assert (
        str(request.url) == "https://api.example.com/api/v1/test"
        "?limit=100&offset=0&order=created&select=id,name&eq(status,active)"
    )


def test_col_mx_iterate_lazy_evaluation(dummy_service):
    """Test lazy evaluation of iterating over resources."""
    response = httpx.Response(
        httpx.codes.OK,
        json={
            "data": [{"id": "ID-1", "name": "Resource 1"}],
            "$meta": {
                "pagination": {
                    "total": 1,
                    "offset": 0,
                    "limit": 100,
                }
            },
        },
    )
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(return_value=response)

        result = dummy_service.iterate()

        assert mock_route.call_count == 0
        first_resource = next(result)
        assert mock_route.call_count == 1
        assert first_resource.id == "ID-1"


def test_col_mx_iterate_handles_api_errors(dummy_service):
    """Test that API errors are handled during iteration over resources."""
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test").mock(
            return_value=httpx.Response(
                httpx.codes.INTERNAL_SERVER_ERROR, json={"error": "Internal Server Error"}
            )
        )
        iterator = dummy_service.iterate()

        with pytest.raises(MPTAPIError):
            list(iterator)


async def test_async_col_mx_fetch_one_success(async_dummy_service, single_result_response):
    """Test fetching a single resource successfully."""
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=single_result_response
        )

        result = await async_dummy_service.fetch_one()

    assert result.id == "ID-1"
    assert result.name == "Test Resource"
    assert mock_route.called
    first_request = mock_route.calls[0].request
    assert "limit=1" in str(first_request.url)
    assert "offset=0" in str(first_request.url)


async def test_async_col_mx_fetch_one_no_results(async_dummy_service, no_results_response):
    """Test fetching a single resource when no results are returned."""
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test").mock(return_value=no_results_response)

        with pytest.raises(ValueError, match="Expected one result, but got zero results"):
            await async_dummy_service.fetch_one()


async def test_async_col_mx_fetch_one_multiple_results(
    async_dummy_service, multiple_results_response
):
    """Test fetching a single resource when multiple results are returned."""
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test").mock(
            return_value=multiple_results_response
        )

        with pytest.raises(ValueError, match=r"Expected one result, but got 2 results"):
            await async_dummy_service.fetch_one()


async def test_async_col_mx_fetch_one_with_filters(
    async_dummy_service, single_result_response, filter_status_active
):
    """Test fetching a single resource with filters applied."""
    filtered_collection = (
        async_dummy_service.filter(filter_status_active).select("id", "name").order_by("created")
    )
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=single_result_response
        )
        result = await filtered_collection.fetch_one()

    assert result.id == "ID-1"
    assert mock_route.called
    first_request = mock_route.calls[0].request
    assert first_request.method == "GET"
    assert first_request.url == (
        "https://api.example.com/api/v1/test"
        "?limit=1&offset=0&order=created"
        "&select=id,name&eq(status,active)"
    )


async def test_async_col_mx_fetch_page_with_filter(
    async_dummy_service, list_response, filter_status_active
) -> None:
    """Test fetching a page of resources with filters applied."""
    custom_collection = (
        async_dummy_service
        .filter(filter_status_active)
        .select("-audit", "product.agreements", "-product.agreements.product")
        .order_by("-created", "name")
    )
    expected_url = (
        "https://api.example.com/api/v1/test?limit=10&offset=5"
        "&order=-created,name"
        "&select=-audit,product.agreements,-product.agreements.product"
        "&eq(status,active)"
    )
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=list_response
        )

        result = await custom_collection.fetch_page(limit=10, offset=5)

    assert result.to_list() == [{"id": "ID-1"}]
    assert mock_route.called
    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.method == "GET"
    assert request.url == expected_url


async def test_async_col_mx_iterate_single_page(async_dummy_service, single_page_response):
    """Test iterating over a single page of resources."""
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=single_page_response
        )

        result = [resource async for resource in async_dummy_service.iterate()]

    request = mock_route.calls[0].request
    assert len(result) == 2
    assert result[0].to_dict() == {"id": "ID-1", "name": "Resource 1"}
    assert result[1].to_dict() == {"id": "ID-2", "name": "Resource 2"}
    assert mock_route.call_count == 1
    assert request.url == "https://api.example.com/api/v1/test?limit=100&offset=0"


async def test_async_col_mx_iterate_multiple_pages(
    async_dummy_service, multi_page_response_page1, multi_page_response_page2
):
    """Test iterating over multiple pages of resources."""
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test", params={"limit": 2, "offset": 0}).mock(
            return_value=multi_page_response_page1
        )
        respx.get("https://api.example.com/api/v1/test", params={"limit": 2, "offset": 2}).mock(
            return_value=multi_page_response_page2
        )

        result = [resource async for resource in async_dummy_service.iterate(2)]

    assert len(result) == 4
    assert result[0].id == "ID-1"
    assert result[1].id == "ID-2"
    assert result[2].id == "ID-3"
    assert result[3].id == "ID-4"


async def test_async_col_mx_iterate_empty_results(async_dummy_service, empty_response):
    """Test iterating over an empty set of resources."""
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=empty_response
        )

        result = [resource async for resource in async_dummy_service.iterate()]

    assert len(result) == 0
    assert mock_route.call_count == 1


async def test_async_col_mx_iterate_no_meta(async_dummy_service, no_meta_response):
    """Test iterating over resources when no metadata is provided."""
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=no_meta_response
        )

        result = [resource async for resource in async_dummy_service.iterate()]

    assert len(result) == 2
    assert result[0].id == "ID-1"
    assert result[1].id == "ID-2"
    assert mock_route.call_count == 1


async def test_async_col_mx_iterate_with_filters(async_dummy_service, filter_status_active):
    """Test iterating over resources with filters applied."""
    filtered_collection = (
        async_dummy_service.filter(filter_status_active).select("id", "name").order_by("created")
    )
    response = httpx.Response(
        httpx.codes.OK,
        json={
            "data": [{"id": "ID-1", "name": "Active Resource"}],
            "$meta": {
                "pagination": {
                    "total": 1,
                    "offset": 0,
                    "limit": 100,
                }
            },
        },
    )
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(return_value=response)

        result = [resource async for resource in filtered_collection.iterate()]

    assert len(result) == 1
    assert result[0].id == "ID-1"
    assert result[0].name == "Active Resource"
    request = mock_route.calls[0].request
    assert (
        str(request.url) == "https://api.example.com/api/v1/test"
        "?limit=100&offset=0&order=created&select=id,name&eq(status,active)"
    )


async def test_async_col_mx_iterate_lazy_evaluation(async_dummy_service):
    """Test lazy evaluation of iterating over resources."""
    response = httpx.Response(
        httpx.codes.OK,
        json={
            "data": [{"id": "ID-1", "name": "Resource 1"}],
            "$meta": {
                "pagination": {
                    "total": 1,
                    "offset": 0,
                    "limit": 100,
                }
            },
        },
    )
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(return_value=response)

        result = async_dummy_service.iterate()

        assert mock_route.call_count == 0
        first_resource = await anext(result)
        assert first_resource.id == "ID-1"
        assert mock_route.call_count == 1


async def test_async_col_mx_iterate_handles_api_errors(async_dummy_service):
    """Test that API errors are handled during iteration over resources."""
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test").mock(
            return_value=httpx.Response(
                httpx.codes.INTERNAL_SERVER_ERROR, json={"error": "Internal Server Error"}
            )
        )

        with pytest.raises(MPTAPIError):
            [resource async for resource in async_dummy_service.iterate()]


@pytest.mark.parametrize(
    "method_name",
    [
        "update",
        "delete",
        "get",
    ],
)
def test_modifieable_resource_mixin(method_name):
    """Test that ModifiableResourceMixin has the required methods."""
    result = _ModifiableResourceService()

    assert hasattr(result, method_name), f"ManagedResourceMixin should have {method_name} method"
    assert callable(getattr(result, method_name)), f"{method_name} should be callable"


@pytest.mark.parametrize(
    "method_name",
    [
        "update",
        "delete",
        "get",
    ],
)
def test_async_modifiable_resource_mixin(method_name):
    """Test that AsyncModifiableResourceMixin has the required methods."""
    result = _AsyncModifiableResourceService()

    assert hasattr(result, method_name), (
        f"AsyncManagedResourceMixin should have {method_name} method"
    )
    assert callable(getattr(result, method_name)), f"{method_name} should be callable"


@pytest.mark.parametrize(
    "method_name",
    [
        "create",
        "update",
        "delete",
        "get",
    ],
)
def test_managed_resource_mixin(method_name):
    """Test that ManagedResourceMixin has the required methods."""
    result = _ManagedService()

    assert hasattr(result, method_name), f"ManagedResourceMixin should have {method_name} method"
    assert callable(getattr(result, method_name)), f"{method_name} should be callable"


@pytest.mark.parametrize(
    "method_name",
    [
        "create",
        "update",
        "delete",
        "get",
    ],
)
def test_async_managed_resource_mixin(method_name):
    """Test that AsyncManagedResourceMixin has the required methods."""
    result = _AsyncManagedService()

    assert hasattr(result, method_name), (
        f"AsyncManagedResourceMixin should have {method_name} method"
    )
    assert callable(getattr(result, method_name)), f"{method_name} should be callable"


class _ModifiableResourceService(ModifiableResourceMixin[DummyModel]):
    """Dummy service class for testing required methods."""


class _AsyncModifiableResourceService(AsyncModifiableResourceMixin[DummyModel]):
    """Dummy service class for testing required methods."""


class _ManagedService(ManagedResourceMixin[DummyModel]):
    """Dummy service class for testing required methods."""


class _AsyncManagedService(AsyncManagedResourceMixin[DummyModel]):
    """Dummy service class for testing required methods."""


def test_sync_file_create_with_resource_data(dummy_file_operations_service):
    """Test creating a file with resource data."""
    file_data = {"id": "FILE-123"}
    with respx.mock:
        mock_route = respx.post("https://api.example.com/public/v1/dummy/file-ops/").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=file_data,
            )
        )
        files = {"file": ("document.pdf", io.BytesIO(b"PDF content"), "application/pdf")}
        resource_data = {"name": "Test Document"}

        result = dummy_file_operations_service.create(resource_data=resource_data, files=files)

        request = mock_route.calls[0].request
    assert b'name="_attachment_data"' in request.content
    assert b'"name":"Test Document"' in request.content
    assert result.to_dict() == file_data


async def test_async_file_create_with_resource_data(async_dummy_file_operations_service):
    """Test creating a file with resource data."""
    file_data = {"id": "FILE-123"}
    with respx.mock:
        mock_route = respx.post("https://api.example.com/public/v1/dummy/file-ops/").mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=file_data,
            )
        )
        files = {"file": ("document.pdf", io.BytesIO(b"PDF content"), "application/pdf")}
        resource_data = {"name": "Test Document"}
        result = await async_dummy_file_operations_service.create(
            resource_data=resource_data, files=files
        )
        request = mock_route.calls[0].request
    assert b'name="_attachment_data"' in request.content
    assert b'"name":"Test Document"' in request.content
    assert result.to_dict() == file_data


def test_sync_update_file(update_file_service):  # noqa: WPS210
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


def test_update_file_no_file(update_file_service):  # noqa: WPS210
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


async def test_async_update_file(async_update_file_service):  # noqa: WPS210
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


async def test_async_update_file_no_file(async_update_file_service):  # noqa: WPS210
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


@pytest.fixture
def async_enablable_service(async_http_client):
    return AsyncEnableDisableService(http_client=async_http_client)


@pytest.fixture
def enablable_service(http_client):
    return EnableDisableService(http_client=http_client)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("enable", {"id": "OBJ-0000-0001", "status": "update"}),
        ("disable", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
def test_enablable_resource_actions(enablable_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/enablable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = getattr(enablable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("enable", None),
        ("disable", None),
    ],
)
def test_enablable_resource_actions_no_data(enablable_service, action, input_status):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/enablable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = getattr(enablable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("enable", {"id": "OBJ-0000-0001", "status": "update"}),
        ("disable", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
async def test_async_enablable_resource_actions(async_enablable_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/enablable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await getattr(async_enablable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("enable", None),
        ("disable", None),
    ],
)
async def test_async_enablable_resource_actions_no_data(
    async_enablable_service, action, input_status
):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/dummy/enablable/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )

        result = await getattr(async_enablable_service, action)("OBJ-0000-0001", input_status)

        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, DummyModel)

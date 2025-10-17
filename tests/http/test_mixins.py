import io
import json

import httpx
import pytest
import respx

from mpt_api_client import RQLQuery
from mpt_api_client.resources.catalog.products_media import (
    AsyncMediaService,
    MediaService,
)


@pytest.fixture
def media_service(http_client):
    return MediaService(http_client=http_client, endpoint_params={"product_id": "PRD-001"})


@pytest.fixture
def async_media_service(async_http_client):
    return AsyncMediaService(
        http_client=async_http_client, endpoint_params={"product_id": "PRD-001"}
    )


async def test_async_create_mixin(async_dummy_service):  # noqa: WPS210
    resource_data = {"name": "Test Resource", "status": "active"}
    new_resource_data = {"id": "new-resource-id", "name": "Test Resource", "status": "active"}
    create_response = httpx.Response(httpx.codes.OK, json=new_resource_data)

    with respx.mock:
        mock_route = respx.post("https://api.example.com/api/v1/test").mock(
            return_value=create_response
        )

        created_resource = await async_dummy_service.create(resource_data)

    assert created_resource.to_dict() == new_resource_data
    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.method == "POST"
    assert request.url == "https://api.example.com/api/v1/test"
    assert json.loads(request.content.decode()) == resource_data


async def test_async_delete_mixin(async_dummy_service):  # noqa: WPS210
    delete_response = httpx.Response(httpx.codes.NO_CONTENT, json=None)

    with respx.mock:
        mock_route = respx.delete("https://api.example.com/api/v1/test/RES-123").mock(
            return_value=delete_response
        )

        await async_dummy_service.delete("RES-123")

    assert mock_route.call_count == 1


async def test_async_update_resource(async_dummy_service):  # noqa: WPS210
    resource_data = {"name": "Test Resource", "status": "active"}
    update_response = httpx.Response(httpx.codes.OK, json=resource_data)

    with respx.mock:
        mock_route = respx.put("https://api.example.com/api/v1/test/RES-123").mock(
            return_value=update_response
        )

        await async_dummy_service.update("RES-123", resource_data)

    request: httpx.Request = mock_route.calls[0].request
    assert mock_route.call_count == 1
    assert json.loads(request.content.decode()) == resource_data


def test_sync_create_mixin(dummy_service):  # noqa: WPS210
    resource_data = {"name": "Test Resource", "status": "active"}
    new_resource_data = {"id": "new-resource-id", "name": "Test Resource", "status": "active"}
    create_response = httpx.Response(httpx.codes.OK, json=new_resource_data)

    with respx.mock:
        mock_route = respx.post("https://api.example.com/api/v1/test").mock(
            return_value=create_response
        )

        created_resource = dummy_service.create(resource_data)

    assert created_resource.to_dict() == new_resource_data
    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.method == "POST"
    assert request.url == "https://api.example.com/api/v1/test"
    assert json.loads(request.content.decode()) == resource_data


def test_sync_delete_mixin(dummy_service):
    delete_response = httpx.Response(httpx.codes.NO_CONTENT, json=None)
    with respx.mock:
        mock_route = respx.delete("https://api.example.com/api/v1/test/RES-123").mock(
            return_value=delete_response
        )

        dummy_service.delete("RES-123")

    assert mock_route.call_count == 1


def test_sync_update_resource(dummy_service):
    resource_data = {"name": "Test Resource", "status": "active"}
    update_response = httpx.Response(httpx.codes.OK, json=resource_data)
    with respx.mock:
        mock_route = respx.put("https://api.example.com/api/v1/test/RES-123").mock(
            return_value=update_response
        )

        dummy_service.update("RES-123", resource_data)

    request = mock_route.calls[0].request
    assert mock_route.call_count == 1
    assert json.loads(request.content.decode()) == resource_data


async def test_async_file_create_with_data(async_media_service):
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
        files = {"media": ("test.jpg", io.BytesIO(b"Image content"), "image/jpeg")}
        new_media = await async_media_service.create({"name": "Product image"}, files=files)

    request: httpx.Request = mock_route.calls[0].request

    assert (
        b'Content-Disposition: form-data; name="_media_data"\r\n'
        b"Content-Type: application/json\r\n\r\n"
        b'{"name":"Product image"}\r\n' in request.content
    )
    assert (
        b'Content-Disposition: form-data; name="media"; filename="test.jpg"\r\n'
        b"Content-Type: image/jpeg\r\n\r\n"
        b"Image content\r\n" in request.content
    )
    assert new_media.to_dict() == media_data


async def test_async_file_create_no_data(async_media_service):
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
        files = {"media": ("test.jpg", io.BytesIO(b"Image content"), "image/jpeg")}
        new_media = await async_media_service.create(files=files)

    request: httpx.Request = mock_route.calls[0].request

    assert (
        b'Content-Disposition: form-data; name="media"; filename="test.jpg"\r\n'
        b"Content-Type: image/jpeg\r\n\r\n"
        b"Image content\r\n" in request.content
    )
    assert new_media.to_dict() == media_data


async def test_async_file_download(async_media_service):
    media_content = b"Image file content or binary data"

    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media/MED-456"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={
                    "content-type": "application/octet-stream",
                    "content-disposition": 'form-data; name="file"; filename="product_image.jpg"',
                },
                content=media_content,
            )
        )

        downloaded_file = await async_media_service.download("MED-456")
        request = mock_route.calls[0].request
        accept_header = (b"Accept", b"*")
        assert accept_header in request.headers.raw
        assert mock_route.call_count == 1
        assert downloaded_file.file_contents == media_content
        assert downloaded_file.content_type == "application/octet-stream"
        assert downloaded_file.filename == "product_image.jpg"


def test_sync_file_download(media_service):
    media_content = b"Image file content or binary data"

    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/public/v1/catalog/products/PRD-001/media/MED-456"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                headers={
                    "content-type": "application/octet-stream",
                    "content-disposition": 'form-data; name="file"; filename="product_image.jpg"',
                },
                content=media_content,
            )
        )

        downloaded_file = media_service.download("MED-456")
        request = mock_route.calls[0].request
        accept_header = (b"Accept", b"*")
        assert accept_header in request.headers.raw
        assert mock_route.call_count == 1
        assert downloaded_file.file_contents == media_content
        assert downloaded_file.content_type == "application/octet-stream"
        assert downloaded_file.filename == "product_image.jpg"


def test_sync_file_create_with_data(media_service):
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
        files = {"media": ("test.jpg", io.BytesIO(b"Image content"), "image/jpeg")}
        new_media = media_service.create({"name": "Product image"}, files=files)

    request: httpx.Request = mock_route.calls[0].request

    assert (
        b'Content-Disposition: form-data; name="_media_data"\r\n'
        b"Content-Type: application/json\r\n\r\n"
        b'{"name":"Product image"}\r\n' in request.content
    )
    assert (
        b'Content-Disposition: form-data; name="media"; filename="test.jpg"\r\n'
        b"Content-Type: image/jpeg\r\n\r\n"
        b"Image content\r\n" in request.content
    )
    assert new_media.to_dict() == media_data


def test_sync_file_create_no_data(media_service):
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
        files = {"media": ("test.jpg", io.BytesIO(b"Image content"), "image/jpeg")}
        new_media = media_service.create(files=files)

    request: httpx.Request = mock_route.calls[0].request

    assert (
        b'Content-Disposition: form-data; name="media"; filename="test.jpg"\r\n'
        b"Content-Type: image/jpeg\r\n\r\n"
        b"Image content\r\n" in request.content
    )
    assert new_media.to_dict() == media_data


@pytest.mark.parametrize(
    "select_value",
    [
        ["id", "name"],
        "id,name",
    ],
)
def test_sync_get_mixin(dummy_service, select_value):
    resource_data = {"id": "RES-123", "name": "Test Resource"}
    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/api/v1/test/RES-123", params={"select": "id,name"}
        ).mock(return_value=httpx.Response(httpx.codes.OK, json=resource_data))

        resource = dummy_service.get("RES-123", select=select_value)

    request = mock_route.calls[0].request
    accept_header = (b"Accept", b"application/json")
    assert accept_header in request.headers.raw
    assert resource.to_dict() == resource_data


async def test_async_get(async_dummy_service):
    resource_data = {"id": "RES-123", "name": "Test Resource"}
    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/api/v1/test/RES-123", params={"select": "id,name"}
        ).mock(return_value=httpx.Response(httpx.codes.OK, json=resource_data))

        resource = await async_dummy_service.get("RES-123", select=["id", "name"])

    request = mock_route.calls[0].request
    accept_header = (b"Accept", b"application/json")
    assert accept_header in request.headers.raw
    assert resource.to_dict() == resource_data


async def test_async_get_select_str(async_dummy_service):
    resource_data = {"id": "RES-123", "name": "Test Resource"}
    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/api/v1/test/RES-123", params={"select": "id,name"}
        ).mock(return_value=httpx.Response(httpx.codes.OK, json=resource_data))

        resource = await async_dummy_service.get("RES-123", select="id,name")

    request = mock_route.calls[0].request
    accept_header = (b"Accept", b"application/json")
    assert accept_header in request.headers.raw
    assert resource.to_dict() == resource_data


def test_queryable_mixin_order_by(dummy_service):
    ordered_service = dummy_service.order_by("created", "-name")

    assert ordered_service != dummy_service
    assert dummy_service.query_state.order_by is None
    assert ordered_service.query_state.order_by == ["created", "-name"]
    assert ordered_service.http_client is dummy_service.http_client
    assert ordered_service.endpoint_params == dummy_service.endpoint_params


def test_queryable_mixin_order_by_exception(dummy_service):
    ordered_service = dummy_service.order_by("created")

    with pytest.raises(
        ValueError, match=r"Ordering is already set. Cannot set ordering multiple times."
    ):
        ordered_service.order_by("name")


def test_queryable_mixin_filter(dummy_service, filter_status_active):
    filtered_service = dummy_service.filter(filter_status_active)

    assert filtered_service != dummy_service
    assert dummy_service.query_state.filter is None
    assert filtered_service.query_state.filter == filter_status_active
    assert filtered_service.http_client is dummy_service.http_client
    assert filtered_service.endpoint_params == dummy_service.endpoint_params


def test_queryable_mixin_filters(dummy_service):
    filter1 = RQLQuery(status="active")
    filter2 = RQLQuery(name="test")

    filtered_service = dummy_service.filter(filter1).filter(filter2)

    assert dummy_service.query_state.filter is None
    assert filtered_service.query_state.filter == filter1 & filter2


def test_queryable_mixin_select(dummy_service):
    selected_service = dummy_service.select("id", "name", "-audit")

    assert selected_service != dummy_service
    assert dummy_service.query_state.select is None
    assert selected_service.query_state.select == ["id", "name", "-audit"]
    assert selected_service.http_client is dummy_service.http_client
    assert selected_service.endpoint_params == dummy_service.endpoint_params


def test_queryable_mixin_select_exception(dummy_service):
    selected_service = dummy_service.select("id", "name")

    with pytest.raises(
        ValueError, match=r"Select fields are already set. Cannot set select fields multiple times."
    ):
        selected_service.select("other_field")


def test_queryable_mixin_method_chaining(dummy_service, filter_status_active):
    chained_service = (
        dummy_service.filter(filter_status_active).order_by("created", "-name").select("id", "name")
    )

    assert chained_service != dummy_service
    assert chained_service.query_state.filter == filter_status_active
    assert chained_service.query_state.order_by == ["created", "-name"]
    assert chained_service.query_state.select == ["id", "name"]

import io
import json

import httpx
import pytest
import respx

from mpt_api_client import RQLQuery
from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.http.mixins import (
    AsyncManagedResourceMixin,
    AsyncModifiableResourceMixin,
    ManagedResourceMixin,
    ModifiableResourceMixin,
)
from mpt_api_client.resources.catalog.products_media import (
    AsyncMediaService,
    MediaService,
)
from tests.conftest import DummyModel


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


def test_col_mx_fetch_one_success(dummy_service, single_result_response):
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=single_result_response
        )

        resource = dummy_service.fetch_one()

    assert resource.id == "ID-1"
    assert resource.name == "Test Resource"
    assert mock_route.called

    first_request = mock_route.calls[0].request
    assert "limit=1" in str(first_request.url)
    assert "offset=0" in str(first_request.url)


def test_col_mx_fetch_one_no_results(dummy_service, no_results_response):
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test").mock(return_value=no_results_response)

        with pytest.raises(ValueError, match="Expected one result, but got zero results"):
            dummy_service.fetch_one()


def test_col_mx_fetch_one_multiple_results(dummy_service, multiple_results_response):
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test").mock(
            return_value=multiple_results_response
        )

        with pytest.raises(ValueError, match=r"Expected one result, but got 2 results"):
            dummy_service.fetch_one()


def test_col_mx_fetch_one_with_filters(dummy_service, single_result_response, filter_status_active):
    filtered_collection = (
        dummy_service.filter(filter_status_active).select("id", "name").order_by("created")
    )

    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=single_result_response
        )
        resource = filtered_collection.fetch_one()

    assert resource.id == "ID-1"
    assert mock_route.called

    first_request = mock_route.calls[0].request
    assert first_request.method == "GET"
    assert first_request.url == (
        "https://api.example.com/api/v1/test"
        "?limit=1&offset=0&order=created"
        "&select=id,name&eq(status,active)"
    )


def test_col_mx_fetch_page_with_filter(dummy_service, list_response, filter_status_active):
    custom_collection = (
        dummy_service.filter(filter_status_active)
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
        collection_results = custom_collection.fetch_page(limit=10, offset=5)

    assert collection_results.to_list() == [{"id": "ID-1"}]
    assert mock_route.called
    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.method == "GET"
    assert request.url == expected_url


def test_col_mx_iterate_single_page(dummy_service, single_page_response):
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=single_page_response
        )

        resources = list(dummy_service.iterate())
        request = mock_route.calls[0].request

    assert len(resources) == 2
    assert resources[0].to_dict() == {"id": "ID-1", "name": "Resource 1"}
    assert resources[1].to_dict() == {"id": "ID-2", "name": "Resource 2"}
    assert mock_route.call_count == 1
    assert request.url == "https://api.example.com/api/v1/test?limit=100&offset=0"


def test_col_mx_iterate_multiple_pages(
    dummy_service, multi_page_response_page1, multi_page_response_page2
):
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test", params={"limit": 2, "offset": 0}).mock(
            return_value=multi_page_response_page1
        )
        respx.get("https://api.example.com/api/v1/test", params={"limit": 2, "offset": 2}).mock(
            return_value=multi_page_response_page2
        )

        resources = list(dummy_service.iterate(2))

    assert len(resources) == 4
    assert resources[0].id == "ID-1"
    assert resources[1].id == "ID-2"
    assert resources[2].id == "ID-3"
    assert resources[3].id == "ID-4"


def test_col_mx_iterate_empty_results(dummy_service, empty_response):
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=empty_response
        )

        resources = list(dummy_service.iterate(2))

    assert len(resources) == 0
    assert mock_route.call_count == 1


def test_col_mx_iterate_no_meta(dummy_service, no_meta_response):
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=no_meta_response
        )

        resources = list(dummy_service.iterate())

    assert len(resources) == 2
    assert resources[0].id == "ID-1"
    assert resources[1].id == "ID-2"
    assert mock_route.call_count == 1


def test_col_mx_iterate_with_filters(dummy_service, filter_status_active):
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

        resources = list(filtered_collection.iterate())

    assert len(resources) == 1
    assert resources[0].id == "ID-1"
    assert resources[0].name == "Active Resource"

    request = mock_route.calls[0].request
    assert (
        str(request.url) == "https://api.example.com/api/v1/test"
        "?limit=100&offset=0&order=created&select=id,name&eq(status,active)"
    )


def test_col_mx_iterate_lazy_evaluation(dummy_service):
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

        iterator = dummy_service.iterate()

        assert mock_route.call_count == 0

        first_resource = next(iterator)

        assert mock_route.call_count == 1
        assert first_resource.id == "ID-1"


def test_col_mx_iterate_handles_api_errors(dummy_service):
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
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=single_result_response
        )

        resource = await async_dummy_service.fetch_one()

    assert resource.id == "ID-1"
    assert resource.name == "Test Resource"
    assert mock_route.called

    first_request = mock_route.calls[0].request
    assert "limit=1" in str(first_request.url)
    assert "offset=0" in str(first_request.url)


async def test_async_col_mx_fetch_one_no_results(async_dummy_service, no_results_response):
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test").mock(return_value=no_results_response)

        with pytest.raises(ValueError, match="Expected one result, but got zero results"):
            await async_dummy_service.fetch_one()


async def test_async_col_mx_fetch_one_multiple_results(
    async_dummy_service, multiple_results_response
):
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test").mock(
            return_value=multiple_results_response
        )

        with pytest.raises(ValueError, match=r"Expected one result, but got 2 results"):
            await async_dummy_service.fetch_one()


async def test_async_col_mx_fetch_one_with_filters(
    async_dummy_service, single_result_response, filter_status_active
):
    filtered_collection = (
        async_dummy_service.filter(filter_status_active).select("id", "name").order_by("created")
    )

    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=single_result_response
        )
        resource = await filtered_collection.fetch_one()

    assert resource.id == "ID-1"
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
    custom_collection = (
        async_dummy_service.filter(filter_status_active)
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
        collection_results = await custom_collection.fetch_page(limit=10, offset=5)

    assert collection_results.to_list() == [{"id": "ID-1"}]
    assert mock_route.called
    assert mock_route.call_count == 1
    request = mock_route.calls[0].request
    assert request.method == "GET"
    assert request.url == expected_url


async def test_async_col_mx_iterate_single_page(async_dummy_service, single_page_response):
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=single_page_response
        )

        resources = [resource async for resource in async_dummy_service.iterate()]

        request = mock_route.calls[0].request

    assert len(resources) == 2
    assert resources[0].to_dict() == {"id": "ID-1", "name": "Resource 1"}
    assert resources[1].to_dict() == {"id": "ID-2", "name": "Resource 2"}
    assert mock_route.call_count == 1
    assert request.url == "https://api.example.com/api/v1/test?limit=100&offset=0"


async def test_async_col_mx_iterate_multiple_pages(
    async_dummy_service, multi_page_response_page1, multi_page_response_page2
):
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test", params={"limit": 2, "offset": 0}).mock(
            return_value=multi_page_response_page1
        )
        respx.get("https://api.example.com/api/v1/test", params={"limit": 2, "offset": 2}).mock(
            return_value=multi_page_response_page2
        )

        resources = [resource async for resource in async_dummy_service.iterate(2)]

    assert len(resources) == 4
    assert resources[0].id == "ID-1"
    assert resources[1].id == "ID-2"
    assert resources[2].id == "ID-3"
    assert resources[3].id == "ID-4"


async def test_async_col_mx_iterate_empty_results(async_dummy_service, empty_response):
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=empty_response
        )

        resources = [resource async for resource in async_dummy_service.iterate()]

    assert len(resources) == 0
    assert mock_route.call_count == 1


async def test_async_col_mx_iterate_no_meta(async_dummy_service, no_meta_response):
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=no_meta_response
        )

        resources = [resource async for resource in async_dummy_service.iterate()]

    assert len(resources) == 2
    assert resources[0].id == "ID-1"
    assert resources[1].id == "ID-2"
    assert mock_route.call_count == 1


async def test_async_col_mx_iterate_with_filters(async_dummy_service, filter_status_active):
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

        resources = [resource async for resource in filtered_collection.iterate()]

    assert len(resources) == 1
    assert resources[0].id == "ID-1"
    assert resources[0].name == "Active Resource"

    request = mock_route.calls[0].request
    assert (
        str(request.url) == "https://api.example.com/api/v1/test"
        "?limit=100&offset=0&order=created&select=id,name&eq(status,active)"
    )


async def test_async_col_mx_iterate_lazy_evaluation(async_dummy_service):
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

        iterator = async_dummy_service.iterate()

        # No requests should be made until we start iterating
        assert mock_route.call_count == 0

        # Get first item to trigger the first request
        first_resource = await anext(iterator)

        assert first_resource.id == "ID-1"
        assert mock_route.call_count == 1


async def test_async_col_mx_iterate_handles_api_errors(async_dummy_service):
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
    class Service(ModifiableResourceMixin[DummyModel]):  # noqa: WPS431
        """Dummy service class for testing required methods."""

    service = Service()

    assert hasattr(service, method_name), f"ManagedResourceMixin should have {method_name} method"
    assert callable(getattr(service, method_name)), f"{method_name} should be callable"


@pytest.mark.parametrize(
    "method_name",
    [
        "update",
        "delete",
        "get",
    ],
)
def test_async_modifiable_resource_mixin(async_dummy_service, method_name):
    class Service(AsyncModifiableResourceMixin[DummyModel]):  # noqa: WPS431
        """Dummy service class for testing required methods."""

    service = Service()

    assert hasattr(service, method_name), (
        f"AsyncManagedResourceMixin should have {method_name} method"
    )
    assert callable(getattr(service, method_name)), f"{method_name} should be callable"


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
    class ManagedService(ManagedResourceMixin[DummyModel]):  # noqa: WPS431
        """Dummy service class for testing required methods."""

    service = ManagedService()

    assert hasattr(service, method_name), f"ManagedResourceMixin should have {method_name} method"
    assert callable(getattr(service, method_name)), f"{method_name} should be callable"


@pytest.mark.parametrize(
    "method_name",
    [
        "create",
        "update",
        "delete",
        "get",
    ],
)
def test_async_managed_resource_mixin(async_dummy_service, method_name):
    class AsyncManagedService(AsyncManagedResourceMixin[DummyModel]):  # noqa: WPS431
        """Dummy service class for testing required methods."""

    async_service = AsyncManagedService()

    assert hasattr(async_service, method_name), (
        f"AsyncManagedResourceMixin should have {method_name} method"
    )
    assert callable(getattr(async_service, method_name)), f"{method_name} should be callable"

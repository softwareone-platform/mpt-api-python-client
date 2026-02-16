import httpx
import pytest
import respx

from mpt_api_client import RQLQuery
from mpt_api_client.exceptions import MPTAPIError
from tests.unit.http.conftest import AsyncDummyService, DummyService


def test_col_mx_fetch_one_success(
    dummy_service: DummyService, single_result_response: httpx.Response
) -> None:
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


def test_col_mx_fetch_one_no_results(
    dummy_service: DummyService, no_results_response: httpx.Response
) -> None:
    """Test fetching a single resource when no results are returned."""
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test").mock(return_value=no_results_response)

        with pytest.raises(ValueError, match="Expected one result, but got zero results"):
            dummy_service.fetch_one()


def test_col_mx_fetch_one_multiple_results(
    dummy_service: DummyService, multiple_results_response: httpx.Response
) -> None:
    """Test fetching a single resource when multiple results are returned."""
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test").mock(
            return_value=multiple_results_response
        )

        with pytest.raises(ValueError, match=r"Expected one result, but got 2 results"):
            dummy_service.fetch_one()


def test_col_mx_fetch_one_with_filters(
    dummy_service: DummyService,
    single_result_response: httpx.Response,
    filter_status_active: RQLQuery,
) -> None:
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
        "&select=id,name&eq(status,'active')"
    )


def test_col_mx_fetch_page_with_filter(
    dummy_service: DummyService, list_response: httpx.Response, filter_status_active: RQLQuery
) -> None:
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
        "&eq(status,'active')"
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


def test_col_mx_iterate_single_page(
    dummy_service: DummyService, single_page_response: httpx.Response
) -> None:
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
    dummy_service: DummyService,
    multi_page_response_page1: httpx.Response,
    multi_page_response_page2: httpx.Response,
) -> None:
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


def test_col_mx_iterate_empty_results(
    dummy_service: DummyService, empty_response: httpx.Response
) -> None:
    """Test iterating over an empty set of resources."""
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=empty_response
        )

        result = list(dummy_service.iterate(2))

    assert len(result) == 0
    assert mock_route.call_count == 1


def test_col_mx_iterate_no_meta(
    dummy_service: DummyService, no_meta_response: httpx.Response
) -> None:
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


def test_col_mx_iterate_with_filters(
    dummy_service: DummyService, filter_status_active: RQLQuery
) -> None:
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
        "?limit=100&offset=0&order=created&select=id,name&eq(status,'active')"
    )


def test_col_mx_iterate_lazy_evaluation(dummy_service: DummyService) -> None:
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


def test_col_mx_iterate_handles_api_errors(dummy_service: DummyService) -> None:
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


async def test_async_col_mx_fetch_one_success(
    async_dummy_service: AsyncDummyService, single_result_response: httpx.Response
) -> None:
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


async def test_async_col_mx_fetch_one_no_results(
    async_dummy_service: AsyncDummyService, no_results_response: httpx.Response
) -> None:
    """Test fetching a single resource when no results are returned."""
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test").mock(return_value=no_results_response)

        with pytest.raises(ValueError, match="Expected one result, but got zero results"):
            await async_dummy_service.fetch_one()


async def test_async_col_mx_fetch_one_multiple_results(
    async_dummy_service: AsyncDummyService, multiple_results_response: httpx.Response
) -> None:
    """Test fetching a single resource when multiple results are returned."""
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test").mock(
            return_value=multiple_results_response
        )

        with pytest.raises(ValueError, match=r"Expected one result, but got 2 results"):
            await async_dummy_service.fetch_one()


async def test_async_col_mx_fetch_one_with_filters(
    async_dummy_service: AsyncDummyService,
    single_result_response: httpx.Response,
    filter_status_active: RQLQuery,
) -> None:
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
        "&select=id,name&eq(status,'active')"
    )


async def test_async_col_mx_fetch_page_with_filter(
    async_dummy_service: AsyncDummyService,
    list_response: httpx.Response,
    filter_status_active: RQLQuery,
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
        "&eq(status,'active')"
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


async def test_async_col_mx_iterate_single_page(
    async_dummy_service: AsyncDummyService, single_page_response: httpx.Response
) -> None:
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
    async_dummy_service: AsyncDummyService,
    multi_page_response_page1: httpx.Response,
    multi_page_response_page2: httpx.Response,
) -> None:
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


async def test_async_col_mx_iterate_empty_results(
    async_dummy_service: AsyncDummyService, empty_response: httpx.Response
) -> None:
    """Test iterating over an empty set of resources."""
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=empty_response
        )

        result = [resource async for resource in async_dummy_service.iterate()]

    assert len(result) == 0
    assert mock_route.call_count == 1


async def test_async_col_mx_iterate_no_meta(
    async_dummy_service: AsyncDummyService, no_meta_response: httpx.Response
) -> None:
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


async def test_async_col_mx_iterate_with_filters(
    async_dummy_service: AsyncDummyService, filter_status_active: RQLQuery
) -> None:
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
        "?limit=100&offset=0&order=created&select=id,name&eq(status,'active')"
    )


async def test_async_col_mx_iterate_lazy_evaluation(async_dummy_service: AsyncDummyService) -> None:
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


async def test_async_col_mx_iterate_handles_api_errors(
    async_dummy_service: AsyncDummyService,
) -> None:
    """Test that API errors are handled during iteration over resources."""
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test").mock(
            return_value=httpx.Response(
                httpx.codes.INTERNAL_SERVER_ERROR, json={"error": "Internal Server Error"}
            )
        )

        with pytest.raises(MPTAPIError):
            [resource async for resource in async_dummy_service.iterate()]

import httpx
import pytest
import respx

from mpt_api_client.rql import RQLQuery


@pytest.fixture
def list_response():
    return httpx.Response(httpx.codes.OK, json={"data": [{"id": "ID-1"}]})


@pytest.fixture
def single_result_response():
    return httpx.Response(
        httpx.codes.OK,
        json={
            "data": [{"id": "ID-1", "name": "Test Resource"}],
            "$meta": {"pagination": {"total": 1, "offset": 0, "limit": 1}},
        },
    )


@pytest.fixture
def no_results_response():
    return httpx.Response(
        httpx.codes.OK,
        json={"data": [], "$meta": {"pagination": {"total": 0, "offset": 0, "limit": 1}}},
    )


@pytest.fixture
def multiple_results_response():
    return httpx.Response(
        200,
        json={
            "data": [{"id": "ID-1", "name": "Resource 1"}, {"id": "ID-2", "name": "Resource 2"}],
            "$meta": {"pagination": {"total": 2, "offset": 0, "limit": 1}},
        },
    )


@pytest.fixture
def filter_status_active():
    return RQLQuery(status="active")


@pytest.mark.asyncio
async def test_fetch_one_success(async_dummy_service, single_result_response):
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


@pytest.mark.asyncio
async def test_fetch_one_no_results(async_dummy_service, no_results_response):
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test").mock(return_value=no_results_response)

        with pytest.raises(ValueError, match="Expected one result, but got zero results"):
            await async_dummy_service.fetch_one()


@pytest.mark.asyncio
async def test_fetch_one_multiple_results(async_dummy_service, multiple_results_response):
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test").mock(
            return_value=multiple_results_response
        )

        with pytest.raises(ValueError, match=r"Expected one result, but got 2 results"):
            await async_dummy_service.fetch_one()


@pytest.mark.asyncio
async def test_fetch_one_with_filters(
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


@pytest.mark.asyncio
async def test_fetch_page_with_filter(
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

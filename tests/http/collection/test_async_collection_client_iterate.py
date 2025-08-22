import httpx
import pytest
import respx

from mpt_api_client.rql import RQLQuery


@pytest.mark.asyncio
async def test_iterate_single_page(async_collection_client, single_page_response):
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=single_page_response
        )

        resources = [resource async for resource in async_collection_client.iterate()]

        request = mock_route.calls[0].request

    assert len(resources) == 2
    assert resources[0].to_dict() == {"id": "ID-1", "name": "Resource 1"}
    assert resources[1].to_dict() == {"id": "ID-2", "name": "Resource 2"}
    assert mock_route.call_count == 1
    assert request.url == "https://api.example.com/api/v1/test?limit=100&offset=0"


@pytest.mark.asyncio
async def test_iterate_multiple_pages(
    async_collection_client, multi_page_response_page1, multi_page_response_page2
):
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test", params={"limit": 2, "offset": 0}).mock(
            return_value=multi_page_response_page1
        )
        respx.get("https://api.example.com/api/v1/test", params={"limit": 2, "offset": 2}).mock(
            return_value=multi_page_response_page2
        )

        resources = [resource async for resource in async_collection_client.iterate(2)]

    assert len(resources) == 4
    assert resources[0].id == "ID-1"
    assert resources[1].id == "ID-2"
    assert resources[2].id == "ID-3"
    assert resources[3].id == "ID-4"


@pytest.mark.asyncio
async def test_iterate_empty_results(async_collection_client, empty_response):
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=empty_response
        )

        resources = [resource async for resource in async_collection_client.iterate()]

    assert len(resources) == 0
    assert mock_route.call_count == 1


@pytest.mark.asyncio
async def test_iterate_no_meta(async_collection_client, no_meta_response):
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=no_meta_response
        )

        resources = [resource async for resource in async_collection_client.iterate()]

    assert len(resources) == 2
    assert resources[0].id == "ID-1"
    assert resources[1].id == "ID-2"
    assert mock_route.call_count == 1


@pytest.mark.asyncio
async def test_iterate_with_filters(async_collection_client):
    filtered_collection = (
        async_collection_client.filter(RQLQuery(status="active"))
        .select("id", "name")
        .order_by("created")
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


@pytest.mark.asyncio
async def test_iterate_lazy_evaluation(async_collection_client):
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

        iterator = async_collection_client.iterate()

        # No requests should be made until we start iterating
        assert mock_route.call_count == 0

        # Get first item to trigger the first request
        first_resource = await anext(iterator)

        assert first_resource.id == "ID-1"
        assert mock_route.call_count == 1

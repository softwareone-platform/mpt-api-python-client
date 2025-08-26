import httpx
import pytest
import respx

from mpt_api_client.rql import RQLQuery


def test_iterate_single_page(dummy_service, single_page_response):
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


def test_iterate_multiple_pages(
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


def test_iterate_empty_results(dummy_service, empty_response):
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=empty_response
        )

        resources = list(dummy_service.iterate(2))

    assert len(resources) == 0
    assert mock_route.call_count == 1


def test_iterate_no_meta(dummy_service, no_meta_response):
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=no_meta_response
        )

        resources = list(dummy_service.iterate())

    assert len(resources) == 2
    assert resources[0].id == "ID-1"
    assert resources[1].id == "ID-2"
    assert mock_route.call_count == 1


def test_iterate_with_filters(dummy_service):
    filtered_collection = (
        dummy_service.filter(RQLQuery(status="active")).select("id", "name").order_by("created")
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


def test_iterate_lazy_evaluation(dummy_service):
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


def test_iterate_handles_api_errors(dummy_service):
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test").mock(
            return_value=httpx.Response(
                httpx.codes.INTERNAL_SERVER_ERROR, json={"error": "Internal Server Error"}
            )
        )

        iterator = dummy_service.iterate()

        with pytest.raises(httpx.HTTPStatusError):
            list(iterator)

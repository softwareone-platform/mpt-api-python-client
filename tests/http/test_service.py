import json

import httpx
import pytest
import respx

from mpt_api_client.rql import RQLQuery
from tests.conftest import DummyModel
from tests.http.conftest import DummyService


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


def test_sync_fetch_one_success(dummy_service, single_result_response):
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


def test_sync_fetch_one_no_results(dummy_service, no_results_response):
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test").mock(return_value=no_results_response)

        with pytest.raises(ValueError, match="Expected one result, but got zero results"):
            dummy_service.fetch_one()


def test_sync_fetch_one_multiple_results(dummy_service, multiple_results_response):
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test").mock(
            return_value=multiple_results_response
        )

        with pytest.raises(ValueError, match=r"Expected one result, but got 2 results"):
            dummy_service.fetch_one()


def test_sync_fetch_one_with_filters(dummy_service, single_result_response, filter_status_active):
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


def test_sync_fetch_page_with_filter(dummy_service, list_response, filter_status_active) -> None:
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


def test_sync_get(dummy_service):
    resource_data = {"id": "RES-123", "name": "Test Resource"}
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test/RES-123").mock(
            return_value=httpx.Response(httpx.codes.OK, json=resource_data)
        )

        resource = dummy_service.get("RES-123", select=["id", "name"])
    assert isinstance(resource, DummyModel)
    assert resource.to_dict() == resource_data


def test_sync_init_defaults(http_client):
    collection_client = DummyService(http_client=http_client)

    assert collection_client.query_rql is None
    assert collection_client.query_order_by is None
    assert collection_client.query_select is None
    assert collection_client.build_url() == "/api/v1/test"


def test_sync_init_with_filter(http_client, filter_status_active):
    collection_client = DummyService(
        http_client=http_client,
        query_rql=filter_status_active,
    )

    assert collection_client.query_rql == filter_status_active
    assert collection_client.query_order_by is None
    assert collection_client.query_select is None
    assert collection_client.build_url() == "/api/v1/test?eq(status,active)"


def test_sync_iterate_single_page(dummy_service, single_page_response):
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


def test_sync_iterate_multiple_pages(
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


def test_sync_iterate_empty_results(dummy_service, empty_response):
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=empty_response
        )

        resources = list(dummy_service.iterate(2))

    assert len(resources) == 0
    assert mock_route.call_count == 1


def test_sync_iterate_no_meta(dummy_service, no_meta_response):
    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test").mock(
            return_value=no_meta_response
        )

        resources = list(dummy_service.iterate())

    assert len(resources) == 2
    assert resources[0].id == "ID-1"
    assert resources[1].id == "ID-2"
    assert mock_route.call_count == 1


def test_sync_iterate_with_filters(dummy_service, filter_status_active):
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


def test_sync_iterate_lazy_evaluation(dummy_service):
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


def test_sync_iterate_handles_api_errors(dummy_service):
    with respx.mock:
        respx.get("https://api.example.com/api/v1/test").mock(
            return_value=httpx.Response(
                httpx.codes.INTERNAL_SERVER_ERROR, json={"error": "Internal Server Error"}
            )
        )

        iterator = dummy_service.iterate()

        with pytest.raises(httpx.HTTPStatusError):
            list(iterator)


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


def test_sync_filter(dummy_service, filter_status_active):
    new_collection = dummy_service.filter(filter_status_active)

    assert dummy_service.query_rql is None
    assert new_collection != dummy_service
    assert new_collection.query_rql == filter_status_active


def test_sync_multiple_filters(dummy_service) -> None:
    filter_query = RQLQuery(status="active")
    filter_query2 = RQLQuery(name="test")

    new_collection = dummy_service.filter(filter_query).filter(filter_query2)

    assert dummy_service.query_rql is None
    assert new_collection.query_rql == filter_query & filter_query2


def test_sync_select(dummy_service) -> None:
    new_collection = dummy_service.select("agreement", "-product")

    assert dummy_service.query_select is None
    assert new_collection != dummy_service
    assert new_collection.query_select == ["agreement", "-product"]


def test_sync_select_exception(dummy_service) -> None:
    with pytest.raises(ValueError):
        dummy_service.select("agreement").select("product")


def test_sync_order_by(dummy_service):
    new_collection = dummy_service.order_by("created", "-name")

    assert dummy_service.query_order_by is None
    assert new_collection != dummy_service
    assert new_collection.query_order_by == ["created", "-name"]


def test_sync_order_by_exception(dummy_service):
    with pytest.raises(
        ValueError, match=r"Ordering is already set. Cannot set ordering multiple times."
    ):
        dummy_service.order_by("created").order_by("name")


def test_sync_url(dummy_service, filter_status_active) -> None:
    custom_collection = (
        dummy_service.filter(filter_status_active)
        .select("-audit", "product.agreements", "-product.agreements.product")
        .order_by("-created", "name")
    )

    url = custom_collection.build_url()

    assert custom_collection != dummy_service
    assert url == (
        "/api/v1/test?order=-created,name"
        "&select=-audit,product.agreements,-product.agreements.product"
        "&eq(status,active)"
    )


def test_sync_clone(dummy_service, filter_status_active) -> None:
    configured = (
        dummy_service.filter(filter_status_active)
        .order_by("created", "-name")
        .select("agreement", "-product")
    )

    cloned = configured.clone()

    assert cloned is not configured
    assert isinstance(cloned, configured.__class__)
    assert cloned.http_client is configured.http_client
    assert str(cloned.query_rql) == str(configured.query_rql)

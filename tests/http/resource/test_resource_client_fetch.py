import httpx
import pytest
import respx


def test_fetch_success(resource_client):
    expected_response = httpx.Response(
        httpx.codes.OK,
        json={"data": {"id": "RES-123", "name": "Test Resource", "status": "active"}},
    )

    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test-resource/RES-123").mock(
            return_value=expected_response
        )

        resource = resource_client.fetch()

    assert resource.to_dict() == {"id": "RES-123", "name": "Test Resource", "status": "active"}
    assert mock_route.called
    assert mock_route.call_count == 1
    assert resource_client.resource_ is not None


def test_get_attribute(resource_client):
    expected_response = httpx.Response(
        httpx.codes.OK,
        json={"data": {"id": "RES-123", "contact": {"name": "Albert"}, "status": "active"}},
    )

    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test-resource/RES-123").mock(
            return_value=expected_response
        )

        assert resource_client.id == "RES-123"
        assert resource_client.contact.name == "Albert"
        assert mock_route.call_count == 1


def test_set_attribute(resource_client):
    expected_response = httpx.Response(
        httpx.codes.OK,
        json={"data": {"id": "RES-123", "contact": {"name": "Albert"}, "status": "active"}},
    )

    with respx.mock:
        respx.get("https://api.example.com/api/v1/test-resource/RES-123").mock(
            return_value=expected_response
        )

        resource_client.status = "disabled"
        resource_client.contact.name = "Alice"

        assert resource_client.status == "disabled"
        assert resource_client.contact.name == "Alice"


def test_fetch_not_found(resource_client):
    error_response = httpx.Response(httpx.codes.NOT_FOUND, json={"error": "Resource not found"})

    with respx.mock:
        respx.get("https://api.example.com/api/v1/test-resource/RES-123").mock(
            return_value=error_response
        )

        with pytest.raises(httpx.HTTPStatusError):
            resource_client.fetch()


def test_fetch_server_error(resource_client):
    error_response = httpx.Response(
        httpx.codes.INTERNAL_SERVER_ERROR, json={"error": "Internal server error"}
    )

    with respx.mock:
        respx.get("https://api.example.com/api/v1/test-resource/RES-123").mock(
            return_value=error_response
        )

        with pytest.raises(httpx.HTTPStatusError):
            resource_client.fetch()


def test_fetch_with_special_characters_in_id(resource_client):
    expected_response = httpx.Response(
        httpx.codes.OK, json={"data": {"id": "RES-123", "name": "Special Resource"}}
    )

    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test-resource/RES-123").mock(
            return_value=expected_response
        )

        resource = resource_client.fetch()

    assert resource.to_dict() == {"id": "RES-123", "name": "Special Resource"}
    assert mock_route.called


def test_fetch_verifies_correct_url_construction(resource_client):
    expected_response = httpx.Response(httpx.codes.OK, json={"data": {"id": "RES-123"}})

    with respx.mock:
        mock_route = respx.get("https://api.example.com/api/v1/test-resource/RES-123").mock(
            return_value=expected_response
        )

        resource_client.fetch()

        request = mock_route.calls[0].request

    assert request.method == "GET"
    assert str(request.url) == "https://api.example.com/api/v1/test-resource/RES-123"

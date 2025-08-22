import re

import httpx
import pytest
import respx


def test_update_resource_successfully(resource_client):
    update_data = {"name": "Updated Resource Name", "status": "modified", "version": 2}
    expected_response = httpx.Response(
        httpx.codes.OK,
        json={
            "data": {
                "id": "RES-123",
                "name": "Updated Resource Name",
                "status": "modified",
                "version": 2,
            }
        },
    )

    with respx.mock:
        mock_route = respx.put("https://api.example.com/api/v1/test-resource/RES-123").mock(
            return_value=expected_response
        )

        resource = resource_client.update(update_data)

    assert resource.to_dict() == {
        "id": "RES-123",
        "name": "Updated Resource Name",
        "status": "modified",
        "version": 2,
    }
    assert mock_route.called
    assert mock_route.call_count == 1


def test_save_resource_successfully(resource_client):
    fetch_response = httpx.Response(
        httpx.codes.OK,
        json={"data": {"id": "RES-123", "name": "Original Name", "status": "active"}},
    )
    save_response = httpx.Response(
        httpx.codes.OK,
        json={"data": {"id": "RES-123", "name": "Modified Name", "status": "active"}},
    )

    with respx.mock:
        respx.get("https://api.example.com/api/v1/test-resource/RES-123").mock(
            return_value=fetch_response
        )
        mock_put_route = respx.put("https://api.example.com/api/v1/test-resource/RES-123").mock(
            return_value=save_response
        )

        resource_client.fetch()
        resource_client.name = "Modified Name"
        resource_client.save()

    assert resource_client.resource_.to_dict() == {
        "id": "RES-123",
        "name": "Modified Name",
        "status": "active",
    }
    assert mock_put_route.called
    assert mock_put_route.call_count == 1


def test_save_raises_error_when_resource_not_set(resource_client):
    expected_message = (
        "Resource data not available. Call fetch() method first to retrieve "
        "the resource `DummyResource`"
    )
    with pytest.raises(RuntimeError, match=re.escape(expected_message)):
        resource_client.save()


def test_delete_resource_successfully(resource_client):
    delete_response = httpx.Response(httpx.codes.NO_CONTENT)

    with respx.mock:
        mock_delete_route = respx.delete(
            "https://api.example.com/api/v1/test-resource/RES-123"
        ).mock(return_value=delete_response)

        resource_client.delete()

    assert resource_client.resource_ is None
    assert mock_delete_route.called
    assert mock_delete_route.call_count == 1

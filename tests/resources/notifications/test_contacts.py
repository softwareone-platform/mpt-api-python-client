import httpx
import pytest
import respx

from mpt_api_client.resources.notifications.contacts import (
    AsyncContactsService,
    ContactsService,
)


@pytest.fixture
def contacts_service(http_client):
    return ContactsService(http_client=http_client)


@pytest.fixture
def async_contacts_service(async_http_client):
    return AsyncContactsService(http_client=async_http_client)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("block", {"id": "CON-123", "status": "to_block"}),
        ("unblock", {"id": "CON-123", "status": "to_unblock"}),
    ],
)
def test_custom_contact_actions(contacts_service, action, input_status):
    request_expected_content = b'{"id":"CON-123","status":"%s"}' % input_status["status"].encode()
    response_expected_data = {"id": "CON-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/notifications/contacts/CON-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        contact = getattr(contacts_service, action)("CON-123", input_status)

        assert mock_route.call_count == 1
        assert contact.to_dict() == response_expected_data
        request = mock_route.calls[0].request
        assert request.content == request_expected_content


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("block", {"id": "CON-123", "status": "to_block"}),
        ("unblock", {"id": "CON-123", "status": "to_unblock"}),
    ],
)
async def test_async_custom_contact_actions(async_contacts_service, action, input_status):
    request_expected_content = b'{"id":"CON-123","status":"%s"}' % input_status["status"].encode()
    response_expected_data = {"id": "CON-123", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/notifications/contacts/CON-123/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "application/json"},
                json=response_expected_data,
            )
        )
        contact = await getattr(async_contacts_service, action)("CON-123", input_status)

        assert contact.to_dict() == response_expected_data
        assert mock_route.call_count == 1
        request = mock_route.calls[0].request
        assert request.content == request_expected_content

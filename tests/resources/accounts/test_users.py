import httpx
import pytest
import respx

from mpt_api_client.resources.accounts.users import AsyncUsersService, User, UsersService


@pytest.fixture
def users_service(http_client):
    return UsersService(http_client=http_client)


@pytest.fixture
def async_users_service(async_http_client):
    return AsyncUsersService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method", ["get", "update", "delete", "block", "unblock", "sso", "sso_check"]
)
def test_mixins_present(users_service, method):
    assert hasattr(users_service, method)


@pytest.mark.parametrize(
    "method", ["get", "update", "delete", "block", "unblock", "sso", "sso_check"]
)
def test_async_mixins_present(async_users_service, method):
    assert hasattr(async_users_service, method)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("sso", {"id": "OBJ-0000-0001", "status": "update"}),
        ("sso_check", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
def test_sso_resource_actions(users_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/"
            f"accounts/users/OBJ-0000-0001/{action.replace('_', '-')}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=response_expected_data,
            )
        )
        blockable_obj = getattr(users_service, action)("OBJ-0000-0001", input_status)

        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert blockable_obj.to_dict() == response_expected_data
        assert isinstance(blockable_obj, User)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("sso", None),
        ("sso_check", None),
    ],
)
def test_sso_resource_actions_no_data(users_service, action, input_status):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/"
            f"accounts/users/OBJ-0000-0001/{action.replace('_', '-')}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=response_expected_data,
            )
        )
        blockable_obj = getattr(users_service, action)("OBJ-0000-0001", input_status)

        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert blockable_obj.to_dict() == response_expected_data
        assert isinstance(blockable_obj, User)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("sso", {"id": "OBJ-0000-0001", "status": "update"}),
        ("sso_check", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
async def test_async_sso_resource_actions(async_users_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/"
            f"accounts/users/OBJ-0000-0001/{action.replace('_', '-')}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=response_expected_data,
            )
        )
        blockable_obj = await getattr(async_users_service, action)("OBJ-0000-0001", input_status)

        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert blockable_obj.to_dict() == response_expected_data
        assert isinstance(blockable_obj, User)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("sso", None),
        ("sso_check", None),
    ],
)
async def test_async_sso_resource_actions_no_data(async_users_service, action, input_status):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            "https://api.example.com/public/v1/"
            f"accounts/users/OBJ-0000-0001/{action.replace('_', '-')}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=response_expected_data,
            )
        )
        blockable_obj = await getattr(async_users_service, action)("OBJ-0000-0001", input_status)

        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert blockable_obj.to_dict() == response_expected_data
        assert isinstance(blockable_obj, User)

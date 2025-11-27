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
    "method", ["get", "update", "delete", "block", "unblock", "sso", "sso_check", "set_password"]
)
def test_mixins_present(users_service, method):
    result = hasattr(users_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method", ["get", "update", "delete", "block", "unblock", "sso", "sso_check", "set_password"]
)
def test_async_mixins_present(async_users_service, method):
    result = hasattr(async_users_service, method)

    assert result is True


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("sso", {"id": "OBJ-0000-0001", "status": "update"}),
        ("sso_check", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
def test_resource_actions(users_service, action, input_status):
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

        result = getattr(users_service, action)("OBJ-0000-0001", input_status)

        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, User)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("sso", None),
        ("sso_check", None),
    ],
)
def test_resource_actions_no_data(users_service, action, input_status):
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

        result = getattr(users_service, action)("OBJ-0000-0001", input_status)

        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, User)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("sso", {"id": "OBJ-0000-0001", "status": "update"}),
        ("sso_check", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
async def test_async_resource_actions(async_users_service, action, input_status):
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

        result = await getattr(async_users_service, action)("OBJ-0000-0001", input_status)

        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, User)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("sso", None),
        ("sso_check", None),
    ],
)
async def test_async_resource_actions_no_data(async_users_service, action, input_status):
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

        result = await getattr(async_users_service, action)("OBJ-0000-0001", input_status)

        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, User)


@pytest.mark.parametrize(
    ("action", "input_password"),
    [
        ("set_password", "new-password-123"),
    ],
)
def test_set_password_action(users_service, action, input_password):
    request_expected_content_str = f'{{"password":"{input_password}"}}'
    request_expected_content = request_expected_content_str.encode()
    response_expected_data = {"password": input_password}
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

        result = getattr(users_service, action)("OBJ-0000-0001", input_password)

        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, User)


@pytest.mark.parametrize(
    ("action", "input_password"),
    [
        ("set_password", "new-password-123"),
    ],
)
async def test_async_set_password_action(async_users_service, action, input_password):
    request_expected_content_str = f'{{"password":"{input_password}"}}'
    request_expected_content = request_expected_content_str.encode()
    response_expected_data = {"password": input_password}
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

        result = await getattr(async_users_service, action)("OBJ-0000-0001", input_password)

        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, User)

import httpx
import pytest
import respx

from mpt_api_client.resources.accounts.buyers import AsyncBuyersService, Buyer, BuyersService


@pytest.fixture
def buyers_service(http_client):
    return BuyersService(http_client=http_client)


@pytest.fixture
def async_buyers_service(async_http_client):
    return AsyncBuyersService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method",
    [
        "get",
        "create",
        "update",
        "delete",
        "activate",
        "deactivate",
        "enable",
        "disable",
        "validate",
        "synchronize",
        "transfer",
    ],
)
def test_mixins_present(buyers_service, method):
    assert hasattr(buyers_service, method)


@pytest.mark.parametrize(
    "method",
    [
        "get",
        "create",
        "update",
        "delete",
        "activate",
        "deactivate",
        "enable",
        "disable",
        "validate",
        "synchronize",
        "transfer",
    ],
)
def test_async_mixins_present(async_buyers_service, method):
    assert hasattr(async_buyers_service, method)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("synchronize", {"id": "OBJ-0000-0001", "status": "update"}),
        ("transfer", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
def test_buyers_resource_action(buyers_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/accounts/buyers/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=response_expected_data,
            )
        )
        buyers_obj = getattr(buyers_service, action)("OBJ-0000-0001", input_status)

        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert buyers_obj.to_dict() == response_expected_data
        assert isinstance(buyers_obj, Buyer)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [("synchronize", None), ("transfer", None)],
)
def test_buyers_resouce_action_no_data(buyers_service, action, input_status):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/accounts/buyers/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=response_expected_data,
            )
        )
        buyers_obj = getattr(buyers_service, action)("OBJ-0000-0001", None)

        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert buyers_obj.to_dict() == response_expected_data
        assert isinstance(buyers_obj, Buyer)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [
        ("synchronize", {"id": "OBJ-0000-0001", "status": "update"}),
        ("transfer", {"id": "OBJ-0000-0001", "status": "update"}),
    ],
)
async def test_async_buyers_resource_action(async_buyers_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/accounts/buyers/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=response_expected_data,
            )
        )
        buyers_obj = await getattr(async_buyers_service, action)("OBJ-0000-0001", input_status)

        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert buyers_obj.to_dict() == response_expected_data
        assert isinstance(buyers_obj, Buyer)


@pytest.mark.parametrize(
    ("action", "input_status"),
    [("synchronize", None), ("transfer", None)],
)
async def test_async_buyers_resource_action_no_data(async_buyers_service, action, input_status):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/accounts/buyers/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=response_expected_data,
            )
        )
        buyers_obj = await getattr(async_buyers_service, action)("OBJ-0000-0001", None)

        request = mock_route.calls[0].request

        assert request.content == request_expected_content
        assert buyers_obj.to_dict() == response_expected_data
        assert isinstance(buyers_obj, Buyer)

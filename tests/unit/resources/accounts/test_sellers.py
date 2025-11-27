import httpx
import pytest
import respx

from mpt_api_client.resources.accounts.sellers import AsyncSellersService, Seller, SellersService


@pytest.fixture
def sellers_service(http_client):
    return SellersService(http_client=http_client)


@pytest.fixture
def async_sellers_service(async_http_client):
    return AsyncSellersService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "activate", "deactivate", "disable"],
)
def test_mixins_present(sellers_service, method):
    result = hasattr(sellers_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "activate", "deactivate", "disable"],
)
def test_async_mixins_present(async_sellers_service, method):
    result = hasattr(async_sellers_service, method)

    assert result is True


@pytest.mark.parametrize(
    ("action", "input_status"), [("disable", {"id": "OBJ-0000-0001", "status": "update"})]
)
def test_sellers_resource_action(sellers_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/accounts/sellers/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=response_expected_data,
            )
        )

        result = getattr(sellers_service, action)("OBJ-0000-0001", input_status)

        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, Seller)


@pytest.mark.parametrize(("action", "input_status"), [("disable", None)])
def test_sellers_resource_action_no_data(sellers_service, action, input_status):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/accounts/sellers/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=response_expected_data,
            )
        )

        result = getattr(sellers_service, action)("OBJ-0000-0001", input_status)

        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, Seller)


@pytest.mark.parametrize(
    ("action", "input_status"), [("disable", {"id": "OBJ-0000-0001", "status": "update"})]
)
async def test_async_sellers_resource_action(async_sellers_service, action, input_status):
    request_expected_content = b'{"id":"OBJ-0000-0001","status":"update"}'
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/accounts/sellers/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=response_expected_data,
            )
        )

        result = await getattr(async_sellers_service, action)("OBJ-0000-0001", input_status)

        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, Seller)


@pytest.mark.parametrize(("action", "input_status"), [("disable", None)])
async def test_async_sellers_resource_action_no_data(async_sellers_service, action, input_status):
    request_expected_content = b""
    response_expected_data = {"id": "OBJ-0000-0001", "status": "new_status"}
    with respx.mock:
        mock_route = respx.post(
            f"https://api.example.com/public/v1/accounts/sellers/OBJ-0000-0001/{action}"
        ).mock(
            return_value=httpx.Response(
                status_code=httpx.codes.OK,
                json=response_expected_data,
            )
        )

        result = await getattr(async_sellers_service, action)("OBJ-0000-0001", input_status)

        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, Seller)

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
    result = hasattr(buyers_service, method)

    assert result is True


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
    result = hasattr(async_buyers_service, method)

    assert result is True


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

        result = getattr(buyers_service, action)("OBJ-0000-0001", input_status)

        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, Buyer)


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

        result = getattr(buyers_service, action)("OBJ-0000-0001", None)

        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, Buyer)


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

        result = await getattr(async_buyers_service, action)("OBJ-0000-0001", input_status)

        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, Buyer)


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

        result = await getattr(async_buyers_service, action)("OBJ-0000-0001", None)

        request = mock_route.calls[0].request
        assert request.content == request_expected_content
        assert result.to_dict() == response_expected_data
        assert isinstance(result, Buyer)


def test_buyers_create(buyers_service, tmp_path):  # noqa: WPS210
    buyer_data = {
        "id": "BUY-0000-0001",
        "name": "Test Buyer",
    }
    logo_path = tmp_path / "logo.png"
    logo_path.write_bytes(b"fake-logo-data")
    with logo_path.open("rb") as logo_file, respx.mock:
        mock_route = respx.post(buyers_service.path).mock(
            return_value=httpx.Response(httpx.codes.CREATED, json=buyer_data)
        )

        result = buyers_service.create(buyer_data, logo=logo_file)

    request = mock_route.calls[0].request
    assert mock_route.call_count == 1
    assert request.method == "POST"
    assert request.url.path == "/public/v1/accounts/buyers"
    assert result.to_dict() == buyer_data


def test_buyers_update(buyers_service, tmp_path):  # noqa: WPS210
    buyer_id = "BUY-0000-0001"
    buyer_data = {
        "name": "Updated Test Buyer",
    }
    logo_path = tmp_path / "logo.png"
    logo_path.write_bytes(b"fake-logo-data")
    with logo_path.open("rb") as logo_file, respx.mock:
        mock_route = respx.put(f"{buyers_service.path}/{buyer_id}").mock(
            return_value=httpx.Response(httpx.codes.OK, json={"id": buyer_id, **buyer_data})
        )

        result = buyers_service.update(buyer_id, buyer_data, logo=logo_file)

    request = mock_route.calls[0].request
    assert mock_route.call_count == 1
    assert request.method == "PUT"
    assert request.url.path == f"/public/v1/accounts/buyers/{buyer_id}"
    assert result.to_dict() == {"id": buyer_id, **buyer_data}


async def test_async_buyers_create(async_buyers_service, tmp_path):  # noqa: WPS210
    buyer_data = {
        "id": "BUY-0000-0001",
        "name": "Test Buyer",
    }
    logo_path = tmp_path / "logo.png"
    logo_path.write_bytes(b"fake-logo-data")
    with logo_path.open("rb") as logo_file, respx.mock:
        mock_route = respx.post(async_buyers_service.path).mock(
            return_value=httpx.Response(httpx.codes.CREATED, json=buyer_data)
        )

        result = await async_buyers_service.create(buyer_data, logo=logo_file)

    request = mock_route.calls[0].request
    assert mock_route.call_count == 1
    assert request.method == "POST"
    assert request.url.path == "/public/v1/accounts/buyers"
    assert result.to_dict() == buyer_data


async def test_async_buyers_update(async_buyers_service, tmp_path):  # noqa: WPS210
    buyer_id = "BUY-0000-0001"
    buyer_data = {
        "name": "Updated Test Buyer",
    }
    logo_path = tmp_path / "logo.png"
    logo_path.write_bytes(b"fake-logo-data")

    with logo_path.open("rb") as logo_file, respx.mock:
        mock_route = respx.put(f"{async_buyers_service.path}/{buyer_id}").mock(
            return_value=httpx.Response(httpx.codes.OK, json={"id": buyer_id, **buyer_data})
        )

        result = await async_buyers_service.update(buyer_id, buyer_data, logo=logo_file)

    request = mock_route.calls[0].request
    assert mock_route.call_count == 1
    assert request.method == "PUT"
    assert request.url.path == f"/public/v1/accounts/buyers/{buyer_id}"
    assert result.to_dict() == {"id": buyer_id, **buyer_data}

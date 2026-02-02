import httpx
import pytest
import respx

from tests.unit.http.conftest import AsyncDummyService, DummyService


@pytest.mark.parametrize(
    "select_value",
    [
        ["id", "name"],
        "id,name",
    ],
)
def test_sync_get_mixin(dummy_service: DummyService, select_value: str | list[str]) -> None:
    """Test getting a resource synchronously with different select parameter formats."""
    resource_data = {"id": "RES-123", "name": "Test Resource"}
    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/api/v1/test/RES-123", params={"select": "id,name"}
        ).mock(return_value=httpx.Response(httpx.codes.OK, json=resource_data))

        result = dummy_service.get("RES-123", select=select_value)

    request = mock_route.calls[0].request
    accept_header = (b"Accept", b"application/json")
    assert accept_header in request.headers.raw
    assert result.to_dict() == resource_data


async def test_async_get(async_dummy_service: AsyncDummyService) -> None:
    """Test getting a resource asynchronously with a list select parameter."""
    resource_data = {"id": "RES-123", "name": "Test Resource"}
    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/api/v1/test/RES-123", params={"select": "id,name"}
        ).mock(return_value=httpx.Response(httpx.codes.OK, json=resource_data))

        result = await async_dummy_service.get("RES-123", select=["id", "name"])

    request = mock_route.calls[0].request
    accept_header = (b"Accept", b"application/json")
    assert accept_header in request.headers.raw
    assert result.to_dict() == resource_data


async def test_async_get_select_str(async_dummy_service: AsyncDummyService) -> None:
    """Test getting a resource asynchronously with a string select parameter."""
    resource_data = {"id": "RES-123", "name": "Test Resource"}
    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/api/v1/test/RES-123", params={"select": "id,name"}
        ).mock(return_value=httpx.Response(httpx.codes.OK, json=resource_data))

        result = await async_dummy_service.get("RES-123", select="id,name")

    request = mock_route.calls[0].request
    accept_header = (b"Accept", b"application/json")
    assert accept_header in request.headers.raw
    assert result.to_dict() == resource_data

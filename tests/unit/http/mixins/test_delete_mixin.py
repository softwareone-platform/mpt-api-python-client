import httpx
import respx

from tests.unit.http.conftest import AsyncDummyService, DummyService


async def test_async_delete_mixin(async_dummy_service: AsyncDummyService) -> None:
    """Test deleting a resource asynchronously."""
    delete_response = httpx.Response(httpx.codes.NO_CONTENT, json=None)
    with respx.mock:
        mock_route = respx.delete("https://api.example.com/api/v1/test/RES-123").mock(
            return_value=delete_response
        )

        await async_dummy_service.delete("RES-123")  # act

    assert mock_route.call_count == 1


def test_sync_delete_mixin(dummy_service: DummyService) -> None:
    """Test deleting a resource synchronously."""
    delete_response = httpx.Response(httpx.codes.NO_CONTENT, json=None)
    with respx.mock:
        mock_route = respx.delete("https://api.example.com/api/v1/test/RES-123").mock(
            return_value=delete_response
        )

        dummy_service.delete("RES-123")  # act

    assert mock_route.call_count == 1

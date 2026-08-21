import httpx
import pytest
import respx

from mpt_api_client.resources.notifications.footers import (
    AsyncFootersService,
    FootersService,
)


@pytest.fixture
def footers_service(http_client):
    return FootersService(http_client=http_client)


@pytest.fixture
def async_footers_service(async_http_client):
    return AsyncFootersService(http_client=async_http_client)


@pytest.fixture
def footer_data():
    return {
        "id": "NFT-1234",
        "languageCode": "en-US",
        "content": "Footer content",
        "isDefault": True,
        "status": "Active",
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


def test_endpoint(footers_service):
    result = footers_service.build_path()

    assert result == "/public/v1/notifications/footers"


def test_async_endpoint(async_footers_service):
    result = async_footers_service.build_path()

    assert result == "/public/v1/notifications/footers"


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate", "fetch_page"])
def test_mixins_present(footers_service, method):
    result = hasattr(footers_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete", "iterate", "fetch_page"])
def test_async_mixins_present(async_footers_service, method):
    result = hasattr(async_footers_service, method)

    assert result is True


def test_get_footer(footers_service, footer_data):
    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/public/v1/notifications/footers/NFT-1234"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "application/json"},
                json=footer_data,
            )
        )

        result = footers_service.get("NFT-1234")

        assert mock_route.call_count == 1
        assert result.id == "NFT-1234"
        assert result.language_code == "en-US"
        assert result.is_default is True
        assert result.status == "Active"


async def test_async_get_footer(async_footers_service, footer_data):
    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/public/v1/notifications/footers/NFT-1234"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "application/json"},
                json=footer_data,
            )
        )

        result = await async_footers_service.get("NFT-1234")

        assert mock_route.call_count == 1
        assert result.to_dict() == footer_data

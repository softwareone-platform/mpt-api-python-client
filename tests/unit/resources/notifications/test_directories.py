import httpx
import pytest
import respx

from mpt_api_client.resources.notifications.directories import (
    AsyncDirectoriesService,
    DirectoriesService,
)


@pytest.fixture
def directories_service(http_client):
    return DirectoriesService(http_client=http_client)


@pytest.fixture
def async_directories_service(async_http_client):
    return AsyncDirectoriesService(http_client=async_http_client)


@pytest.fixture
def directory_data():
    return {
        "id": "NDR-1234",
        "type": "Vendor",
        "account": {"id": "ACC-1234", "name": "Account"},
        "origin": {"id": "ACC-5678", "name": "Origin account"},
        "contacts": [{"id": "CON-1234", "email": "contact@example.com"}],
        "audit": {"created": {"at": "2024-01-01T00:00:00Z"}},
    }


def test_endpoint(directories_service):
    result = directories_service.build_path()

    assert result == "/public/v1/notifications/directories"


def test_async_endpoint(async_directories_service):
    result = async_directories_service.build_path()

    assert result == "/public/v1/notifications/directories"


@pytest.mark.parametrize("method", ["get", "iterate", "fetch_page"])
def test_mixins_present(directories_service, method):
    result = hasattr(directories_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "iterate", "fetch_page"])
def test_async_mixins_present(async_directories_service, method):
    result = hasattr(async_directories_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["create", "update", "delete"])
def test_write_mixins_absent(directories_service, method):
    result = hasattr(directories_service, method)

    assert result is False


@pytest.mark.parametrize("method", ["create", "update", "delete"])
def test_async_write_mixins_absent(async_directories_service, method):
    result = hasattr(async_directories_service, method)

    assert result is False


def test_get_directory(directories_service, directory_data):
    with respx.mock:
        mock_route = respx.get(
            "https://api.example.com/public/v1/notifications/directories/NDR-1234"
        ).mock(
            return_value=httpx.Response(
                status_code=200,
                headers={"content-type": "application/json"},
                json=directory_data,
            )
        )

        result = directories_service.get("NDR-1234")

        assert mock_route.call_count == 1
        assert result.to_dict() == directory_data
        assert result.account.id == "ACC-1234"
        assert result.contacts[0].id == "CON-1234"

import pytest

from mpt_api_client.resources.accounts.licensees import AsyncLicenseesService, LicenseesService


@pytest.fixture
def licensees_service(http_client):
    return LicenseesService(http_client=http_client)


@pytest.fixture
def async_licensees_service(async_http_client):
    return AsyncLicenseesService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "delete", "update", "enable", "disable"],
)
def test_licensees_mixins_present(licensees_service, method):
    assert hasattr(licensees_service, method)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "delete", "update", "enable", "disable"],
)
def test_async_licensees_mixins_present(async_licensees_service, method):
    assert hasattr(async_licensees_service, method)

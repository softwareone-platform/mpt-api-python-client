import pytest

from mpt_api_client.resources.accounts.erp_links import AsyncErpLinksService, ErpLinksService


@pytest.fixture
def erp_links_service(http_client):
    return ErpLinksService(http_client=http_client)


@pytest.fixture
def async_erp_links_service(async_http_client):
    return AsyncErpLinksService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "block", "unblock"],
)
def test_mixins_present(erp_links_service, method):
    result = hasattr(erp_links_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "block", "unblock"],
)
def test_async_mixins_present(async_erp_links_service, method):
    result = hasattr(async_erp_links_service, method)

    assert result is True

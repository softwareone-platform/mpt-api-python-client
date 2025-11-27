import pytest

from mpt_api_client.resources.accounts.api_tokens import (
    ApiTokensService,
    AsyncApiTokensService,
)


@pytest.fixture
def api_tokens_service(http_client):
    return ApiTokensService(http_client=http_client)


@pytest.fixture
def async_api_tokens_service(async_http_client):
    return AsyncApiTokensService(http_client=async_http_client)


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "enable", "disable"],
)
def test_api_tokens_mixins_present(api_tokens_service, method):
    result = hasattr(api_tokens_service, method)

    assert result is True


@pytest.mark.parametrize(
    "method",
    ["get", "create", "update", "delete", "enable", "disable"],
)
def test_async_api_tokens_mixins_present(async_api_tokens_service, method):
    result = hasattr(async_api_tokens_service, method)

    assert result is True

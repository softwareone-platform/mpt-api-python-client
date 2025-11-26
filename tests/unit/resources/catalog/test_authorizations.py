import pytest

from mpt_api_client.resources.catalog.authorizations import (
    AsyncAuthorizationsService,
    AuthorizationsService,
)


@pytest.fixture
def authorizations_service(http_client):
    return AuthorizationsService(http_client=http_client)


@pytest.fixture
def async_authorizations_service(async_http_client):
    return AsyncAuthorizationsService(http_client=async_http_client)


@pytest.mark.parametrize("method", ["get", "create", "update", "delete"])
def test_mixins_present(authorizations_service, method):
    result = hasattr(authorizations_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get", "create", "update", "delete"])
def test_async_mixins_present(async_authorizations_service, method):
    result = hasattr(async_authorizations_service, method)

    assert result is True

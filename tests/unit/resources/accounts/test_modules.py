import pytest

from mpt_api_client.resources.accounts.modules import AsyncModulesService, ModulesService


@pytest.fixture
def module_service(http_client):
    return ModulesService(http_client=http_client)


@pytest.fixture
def async_module_service(http_client):
    return AsyncModulesService(http_client=http_client)


@pytest.mark.parametrize("method", ["get"])
def test_modules_mixins_present(module_service, method):
    result = hasattr(module_service, method)

    assert result is True


@pytest.mark.parametrize("method", ["get"])
def test_async_modules_mixins_present(async_module_service, method):
    result = hasattr(async_module_service, method)

    assert result is True

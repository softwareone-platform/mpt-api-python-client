from unittest.mock import AsyncMock, patch

import pytest

from mpt_api_client.resources.accounts.modules import AsyncModulesService, Module
from seed.accounts.module import get_module, refresh_module, seed_module
from seed.context import Context


@pytest.fixture
def module():
    return Module({"id": "MOD-123", "name": "Test Module"})


@pytest.fixture
def modules_service():
    return AsyncMock(spec=AsyncModulesService)


async def test_get_module(
    context: Context, operations_client, module, modules_service
) -> None:
    context["accounts.module.id"] = module.id
    modules_service.get.return_value = module
    operations_client.accounts.modules = modules_service

    result = await get_module(context=context, mpt_operations=operations_client)

    assert result == module
    assert context.get_resource("accounts.module", module.id) == module


async def test_get_module_without_id(context: Context) -> None:
    result = await get_module(context=context)
    assert result is None


async def test_refresh_module(
    context: Context, operations_client, modules_service, module
) -> None:
    modules_service.refresh.return_value = module
    operations_client.accounts.modules = modules_service

    result = await refresh_module(context, mpt_operations=operations_client)

    assert result == module
    modules_service.refresh.assert_called_once()


async def test_refresh_module_get_new(
    context: Context, operations_client, modules_service, module
) -> None:
    modules_service.refresh.return_value = module
    operations_client.accounts.modules = modules_service
    with patch("seed.accounts.module.get_module", return_value=None):
        result = await refresh_module(context, mpt_operations=operations_client)

        assert result == module
        modules_service.refresh.assert_called_once()


async def test_seed_module() -> None:
    with (
        patch("seed.accounts.module.refresh_module", new_callable=AsyncMock) as mock_refresh_module,
    ):
        await seed_module()  # act

        mock_refresh_module.assert_awaited_once()

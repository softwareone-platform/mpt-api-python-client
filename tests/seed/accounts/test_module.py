import pytest

from mpt_api_client.resources.accounts.modules import AsyncModulesService, Module
from seed.accounts.module import get_module, refresh_module, seed_module
from seed.context import Context


class DummyAsyncIterator:
    def __init__(self, modules):
        self._iterator = iter(modules)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self._iterator)
        except StopIteration as err:
            raise StopAsyncIteration from err


@pytest.fixture
def module():
    return Module({"id": "MOD-123", "name": "Test Module"})


@pytest.fixture
def modules_service(mocker):
    return mocker.Mock(spec=AsyncModulesService)


def async_iter(iter_items):
    yield from iter_items


async def test_get_module(context: Context, operations_client, module, modules_service):
    context["accounts.module.id"] = module.id
    modules_service.get.return_value = module
    operations_client.accounts.modules = modules_service

    result = await get_module(context=context, mpt_operations=operations_client)

    assert result == module
    assert context.get_resource("accounts.module", module.id) == module


async def test_get_module_without_id(context: Context):
    result = await get_module(context=context)
    assert result is None


async def test_refresh_module(context: Context, operations_client, modules_service, module, mocker):
    modules_service.refresh = mocker.AsyncMock(return_value=module)
    operations_client.accounts.modules = modules_service
    context["accounts.module.id"] = module.id
    mock_get_module = mocker.patch("seed.accounts.module.get_module", new_callable=mocker.AsyncMock)
    mocker.patch("seed.accounts.module.Module", new=Module)
    mocker.patch.object(
        operations_client.accounts.modules, "filter", return_value=mocker.AsyncMock()
    )
    mock_get_module.return_value = None
    modules_filter = operations_client.accounts.modules.filter
    modules_filter.return_value.iterate = lambda: DummyAsyncIterator([module])
    result = await refresh_module(context=context, mpt_operations=operations_client)
    assert result == module


async def test_refresh_module_get_new(
    context: Context, operations_client, modules_service, module, mocker
):
    modules_service.refresh = mocker.AsyncMock(return_value=module)
    operations_client.accounts.modules = modules_service
    context["accounts.module.id"] = module.id
    mock_get_module = mocker.patch("seed.accounts.module.get_module", new_callable=mocker.AsyncMock)
    mocker.patch("seed.accounts.module.Module", new=Module)
    mocker.patch.object(
        operations_client.accounts.modules, "filter", return_value=mocker.AsyncMock()
    )
    mock_get_module.return_value = None
    modules_filter = operations_client.accounts.modules.filter
    modules_filter.return_value.iterate = lambda: DummyAsyncIterator([module])
    result = await refresh_module(context=context, mpt_operations=operations_client)
    assert result == module


async def test_seed_module(mocker):
    mock_get_module = mocker.patch("seed.accounts.module.get_module", new_callable=mocker.AsyncMock)
    mock_refresh_module = mocker.patch(
        "seed.accounts.module.refresh_module", new_callable=mocker.AsyncMock
    )
    mock_get_module.return_value = None
    await seed_module()
    mock_refresh_module.assert_awaited_once()

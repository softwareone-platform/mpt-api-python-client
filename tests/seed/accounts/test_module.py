import pytest

from mpt_api_client.resources.accounts.modules import AsyncModulesService, Module
from seed.accounts.module import refresh_module, seed_module
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
def context_with_data() -> Context:
    ctx = Context()
    ctx["accounts.module.id"] = "MOD-123"
    return ctx


@pytest.fixture
def module():
    return Module({"id": "MOD-123", "name": "Test Module"})


@pytest.fixture
def modules_service(mocker):
    return mocker.Mock(spec=AsyncModulesService)


def async_iter(iter_items):
    yield from iter_items


async def test_refresh_module(
    context_with_data, operations_client, modules_service, module, mocker
):
    modules_service.refresh = mocker.AsyncMock(return_value=module)
    operations_client.accounts.modules = modules_service
    mocker.patch("seed.accounts.module.Module", new=Module)
    mocker.patch.object(
        operations_client.accounts.modules, "filter", return_value=mocker.AsyncMock()
    )
    modules_filter = operations_client.accounts.modules.filter
    modules_filter.return_value.iterate = lambda: DummyAsyncIterator([module])
    result = await refresh_module(context=context_with_data, mpt_operations=operations_client)
    assert result == module


async def test_seed_module(mocker):
    mock_init_resource = mocker.patch(
        "seed.accounts.module.init_resource", new_callable=mocker.AsyncMock
    )

    await seed_module()

    mock_init_resource.assert_awaited_once()

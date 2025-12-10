import pytest

from mpt_api_client.resources.accounts.modules import AsyncModulesService, Module
from seed.accounts.module import find_module, seed_module


class DummyAsyncIterator:
    def __init__(self, items):  # noqa: WPS110
        self._iterator = iter(items)  # noqa: WPS110

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


async def test_find_module(operations_client, module, modules_service, mocker):
    operations_client.accounts.modules = modules_service
    mocker.patch.object(
        operations_client.accounts.modules, "filter", return_value=mocker.AsyncMock()
    )
    modules_filter = operations_client.accounts.modules.filter
    modules_filter.return_value.iterate = lambda: DummyAsyncIterator([module])

    result = await find_module(mpt_operations=operations_client)

    assert result == module


async def test_find_module_not_found(operations_client, modules_service, mocker):
    operations_client.accounts.modules = modules_service
    mocker.patch.object(
        operations_client.accounts.modules, "filter", return_value=mocker.AsyncMock()
    )
    modules_filter = operations_client.accounts.modules.filter
    modules_filter.return_value.iterate = lambda: DummyAsyncIterator([])

    with pytest.raises(ValueError, match=r"Module 'Access Management' not found."):
        await find_module(mpt_operations=operations_client)


async def test_seed_module(mocker):
    init_resource = mocker.patch("seed.accounts.module.init_resource", autospec=True)

    await seed_module()  # act

    init_resource.assert_awaited_once()

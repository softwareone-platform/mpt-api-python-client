import pytest

from seed.catalog.price_list import create_price_list, seed_price_list
from seed.context import Context


@pytest.fixture
def context_with_product():
    ctx = Context()
    ctx["catalog.product.id"] = "prod-123"
    return ctx


async def test_create_price_list(mocker, operations_client, context_with_product):
    create_mock = mocker.AsyncMock(return_value={"id": "pl-1"})
    operations_client.catalog.price_lists.create = create_mock

    result = await create_price_list(operations_client, context_with_product)

    assert result == {"id": "pl-1"}
    args, _ = create_mock.await_args
    payload = args[0]
    assert payload["product"]["id"] == "prod-123"


async def test_seed_price_list_create(mocker):
    init_resource = mocker.patch(
        "seed.catalog.price_list.init_resource",
        new_callable=mocker.AsyncMock,
        return_value=mocker.Mock(id="pl-999"),
    )

    await seed_price_list()

    init_resource.assert_awaited_once_with("catalog.price_list.id", create_price_list)

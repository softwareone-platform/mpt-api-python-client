import pytest

from seed.catalog.price_list import create_price_list, seed_price_list
from seed.context import Context


@pytest.fixture
def context_with_product():
    """
    Create a Context pre-populated with a product identifier for tests.
    
    Returns:
        Context: A Context instance with "catalog.product.id" set to "prod-123".
    """
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


async def test_seed_price_list_skips(mocker, context_with_product):
    context_with_product["catalog.price_list.id"] = "pl-123"
    create_mock = mocker.patch(
        "seed.catalog.price_list.create_price_list", new_callable=mocker.AsyncMock
    )

    await seed_price_list(context_with_product)

    create_mock.assert_not_called()


async def test_seed_price_list_create(mocker, context_with_product):
    create_mock = mocker.patch(
        "seed.catalog.price_list.create_price_list",
        new_callable=mocker.AsyncMock,
        return_value=mocker.Mock(id="pl-999"),
    )

    await seed_price_list(context_with_product)

    create_mock.assert_awaited_once()
    assert context_with_product.get_string("catalog.price_list.id") == "pl-999"
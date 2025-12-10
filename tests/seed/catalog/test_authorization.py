import pytest

from seed.catalog.authorization import create_authorization, seed_authorization
from seed.context import Context


@pytest.fixture
def context_with_data() -> Context:
    ctx = Context()
    ctx["catalog.product.id"] = "prod-123"
    ctx["accounts.seller.id"] = "seller-456"
    ctx["accounts.account.id"] = "acct-321"
    return ctx


async def test_create_authorization(mocker, operations_client, context_with_data):
    create_mock = mocker.AsyncMock(return_value={"id": "auth-1"})
    operations_client.catalog.authorizations.create = create_mock
    fake_uuid = mocker.Mock(hex="cafebabe12345678")
    mocker.patch("uuid.uuid4", return_value=fake_uuid)

    result = await create_authorization(operations_client, context_with_data)

    assert result == {"id": "auth-1"}
    args, _ = create_mock.await_args
    payload = args[0]
    assert payload["product"]["id"] == "prod-123"
    assert payload["owner"]["id"] == "seller-456"
    assert payload["vendor"]["id"] == "acct-321"


async def test_seed_authorization(mocker):
    init_resource = mocker.patch(
        "seed.catalog.authorization.init_resource",
        autospec=True,
    )

    await seed_authorization()

    init_resource.assert_awaited_once_with("catalog.authorization.id", create_authorization)

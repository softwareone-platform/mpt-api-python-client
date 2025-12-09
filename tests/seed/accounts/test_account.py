import pytest

from seed.accounts.account import init_account_id, seed_account_ids
from seed.context import Context


@pytest.fixture
def context_without_data() -> Context:
    return Context()


@pytest.mark.parametrize(
    ("env_var", "env_value"),
    [
        ("VENDOR_ACCOUNT_ID", "vendor-789"),
        ("CLIENT_ACCOUNT_ID", "client-012"),
        ("OPERATIONS_ACCOUNT_ID", "ops-345"),
    ],
)
async def test_init_account_id(monkeypatch, context_without_data, env_var, env_value):
    monkeypatch.setenv(env_var, env_value)
    result = await init_account_id(env_var, context=context_without_data)
    assert result == env_value


async def test_seed_account_ids(mocker):
    init_resource = mocker.patch(
        "seed.accounts.account.init_resource",
        new_callable=mocker.AsyncMock,
    )

    await seed_account_ids()

    init_resource.assert_any_call("accounts.account.id", mocker.ANY)
    init_resource.assert_any_call("accounts.client_account.id", mocker.ANY)
    init_resource.assert_any_call("accounts.operations_account.id", mocker.ANY)

import pytest

pytestmark = [pytest.mark.flaky]


async def test_installations_token_account_scoped(
    async_installations_token_service, installation_account_id
):
    result = await async_installations_token_service.token(installation_account_id)

    assert result.token


async def test_installations_token(async_installations_token_service):
    result = await async_installations_token_service.token()

    assert result.token

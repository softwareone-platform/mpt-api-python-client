import pytest

pytestmark = [pytest.mark.flaky]


def test_installations_token_account_scoped(installations_token_service, installation_account_id):
    result = installations_token_service.token(installation_account_id)

    assert result.token


def test_installations_token(installations_token_service):
    result = installations_token_service.token()

    assert result.token

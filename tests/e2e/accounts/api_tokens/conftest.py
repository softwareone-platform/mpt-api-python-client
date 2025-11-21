import pytest


@pytest.fixture
def api_token_id(e2e_config):
    return e2e_config["accounts.api_token.id"]


@pytest.fixture
def invalid_api_token_id():
    return "TKN-0000-0000"


@pytest.fixture
def api_token_factory(account_id, module_id):
    def _api_token(
        name: str = "E2E Test API Token",
        description: str = "E2E API Token created during E2E tests",
    ):
        return {
            "account": {"id": account_id},
            "name": name,
            "description": description,
            "icon": "",
            "modules": [{"id": module_id}],
        }

    return _api_token

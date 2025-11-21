import pytest
import uuid


@pytest.fixture
def invalid_user_id():
    return "USR-0000-0000"


@pytest.fixture
def account_user_factory(account_id, user_group_id):
    def _account_user(
        email: str = f"e2e_{uuid.uuid4()!s}@dummy.com",  # Must be unique in Marketplace
        first_name: str = "E2E Created",
        last_name: str = "Account User",
    ):
        return {
            "user": {
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
            },
            "account": {
                "id": account_id,
            },
            "groups": [
                {"id": user_group_id},
            ],
            "invitation": {
                "status": "Invited",
            }
        }

    return _account_user

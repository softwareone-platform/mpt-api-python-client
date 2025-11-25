import pytest


@pytest.fixture
def licensee_account_id(e2e_config):
    return e2e_config["accounts.licensee.account.id"]


@pytest.fixture
def licensee_group_id(e2e_config):
    return e2e_config["accounts.licensee.group.id"]


@pytest.fixture
def invalid_licensee_id():
    return "LCE-0000-0000-0000"


@pytest.fixture
def licensee_factory(seller_id, buyer_id, user_group_factory, licensee_account_id):
    def _licensee(
        name: str = "Test E2E Licensee",
        licensee_type: str = "Client",
    ):
        group = user_group_factory(user_group_account_id=licensee_account_id)

        return {
            "name": name,
            "address": {
                "addressLine1": "123 Main St",
                "city": "Los Angeles",
                "state": "CA",
                "postCode": "67890",
                "country": "US",
            },
            "useBuyerAddress": False,
            "seller": {"id": seller_id},
            "buyer": {"id": buyer_id},
            "account": {"id": licensee_account_id},
            "eligibility": {"client": True, "partner": False},
            "groups": [group],
            "type": licensee_type,
            "status": "Enabled",
            "defaultLanguage": "en-US",
        }

    return _licensee

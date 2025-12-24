import pytest


@pytest.fixture
def invalid_billing_journal_id():
    return "BJO-0000-0000"


@pytest.fixture
def billing_journal_factory(authorization_id):
    def factory(
        name: str = "E2E Created Billing Journal",
    ):
        return {
            "authorization": {"id": authorization_id},
            "dueDate": "2026-01-02T19:00:00.000Z",
            "externalIds": {},
            "name": name,
        }

    return factory

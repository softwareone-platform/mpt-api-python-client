import pytest


@pytest.fixture
def subscriber_id(e2e_config):
    return e2e_config.get("notifications.subscriber.id")


@pytest.fixture
def invalid_subscriber_id():
    return "NTS-0000-0000-0000"


@pytest.fixture
def recipients_factory(user_id, user_group_id):
    def _recipients(  # noqa: WPS430
        users: list | None = None,
        user_groups: list | None = None,
    ) -> dict:
        return {
            "users": users or [{"id": user_id}],
            "userGroups": user_groups or [{"id": user_group_id}],
        }

    return _recipients


@pytest.fixture
def subscriber_factory(recipients_factory):
    def _subscriber(  # noqa: WPS430
        recipients: dict | None = None,
        note: str = "Test note",
    ) -> dict:
        return {
            "recipients": recipients or recipients_factory(),
            "note": note,
        }

    return _subscriber

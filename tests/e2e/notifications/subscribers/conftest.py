import pytest

from mpt_api_client.exceptions import MPTAPIError


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


@pytest.fixture
def disabled_subscriber_id(mpt_client, subscriber_id):
    subscriber = mpt_client.notifications.subscribers.get(subscriber_id)
    if subscriber.status != "Disabled":
        subscriber = mpt_client.notifications.subscribers.disable(subscriber_id)

    yield subscriber.id

    try:
        mpt_client.notifications.subscribers.enable(subscriber_id)
    except MPTAPIError:
        print(f"TEARDOWN - Unable to re-enable subscriber {subscriber_id=}")  # noqa: WPS421


@pytest.fixture
def active_subscriber_id(mpt_client, subscriber_id):
    subscriber = mpt_client.notifications.subscribers.get(subscriber_id)
    if subscriber.status != "Active":
        subscriber = mpt_client.notifications.subscribers.enable(subscriber_id)

    return subscriber.id

import pytest


@pytest.fixture
def batch_service(mpt_ops):
    return mpt_ops.notifications.batches


@pytest.fixture
def async_batch_service(async_mpt_ops):
    return async_mpt_ops.notifications.batches


@pytest.fixture
def batch_id(e2e_config):
    return e2e_config["notifications.batch.id"]


@pytest.fixture
def batch_data(category_id, short_uuid):
    return {
        "category": {"id": category_id},
        "subject": f"E2E - please delete - {short_uuid}",
        "body": "Hello world",
        "contacts": [{"email": f"{short_uuid}@example.com"}],
    }

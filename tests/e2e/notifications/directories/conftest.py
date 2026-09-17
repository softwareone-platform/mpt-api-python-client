import pytest


@pytest.fixture
def directories_service(mpt_ops):
    return mpt_ops.notifications.directories


@pytest.fixture
def async_directories_service(async_mpt_ops):
    return async_mpt_ops.notifications.directories


@pytest.fixture(scope="session")
def directory_id(e2e_config):
    return e2e_config["notifications.directory.id"]

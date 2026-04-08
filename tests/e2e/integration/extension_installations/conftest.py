import pytest


@pytest.fixture(scope="session")
def extension_id(e2e_config):
    return e2e_config["integration.extension.id"]


@pytest.fixture
def extension_installations_service(mpt_ops, extension_id):
    return mpt_ops.integration.extensions.installations(extension_id)


@pytest.fixture
def async_extension_installations_service(async_mpt_ops, extension_id):
    return async_mpt_ops.integration.extensions.installations(extension_id)

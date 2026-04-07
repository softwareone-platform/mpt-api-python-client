import pytest


@pytest.fixture(scope="session")
def extension_id(e2e_config):
    return e2e_config["integration.extension.id"]


@pytest.fixture
def extension_instances_service(mpt_ops, extension_id):
    return mpt_ops.integration.extensions.instances(extension_id)


@pytest.fixture
def async_extension_instances_service(async_mpt_ops, extension_id):
    return async_mpt_ops.integration.extensions.instances(extension_id)


@pytest.fixture
def instance_data(short_uuid):
    return {
        "externalId": f"e2e-instance-{short_uuid}",
        "version": "1.0.0",
    }

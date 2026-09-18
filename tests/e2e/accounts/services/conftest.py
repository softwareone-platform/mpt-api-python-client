import pytest


@pytest.fixture
def services_service(mpt_ops):
    return mpt_ops.accounts.services


@pytest.fixture
def async_services_service(async_mpt_ops):
    return async_mpt_ops.accounts.services


@pytest.fixture(scope="session")
def service_id(e2e_config):
    return e2e_config["accounts.service.id"]


@pytest.fixture
def invalid_service_id():
    return "SVC-0000"

import pytest


@pytest.fixture
def pairs_service(mpt_ops):
    return mpt_ops.exchange.pairs


@pytest.fixture
def async_pairs_service(async_mpt_ops):
    return async_mpt_ops.exchange.pairs


@pytest.fixture(scope="session")
def pair_id(e2e_config):
    return e2e_config["exchange.pair.id"]

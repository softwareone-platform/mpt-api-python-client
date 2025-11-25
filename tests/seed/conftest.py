import io

import pytest

from mpt_api_client import AsyncMPTClient
from seed.context import Context


def fake_file():
    return io.BytesIO(b"fake data")


@pytest.fixture
def context() -> Context:
    return Context()


@pytest.fixture
def vendor_client(mocker):
    return mocker.Mock(spec=AsyncMPTClient)


@pytest.fixture
def operations_client(mocker):
    return mocker.Mock(spec=AsyncMPTClient)


@pytest.fixture
def client_client(mocker):
    return mocker.Mock(spec=AsyncMPTClient)


@pytest.fixture
def fake_file_factory():
    return fake_file

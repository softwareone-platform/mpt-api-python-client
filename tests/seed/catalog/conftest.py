from unittest.mock import AsyncMock, MagicMock

import pytest

from mpt_api_client import AsyncMPTClient
from seed.context import Context


@pytest.fixture
def context() -> Context:
    return Context()


@pytest.fixture
def vendor_client() -> AsyncMock:
    return MagicMock(spec=AsyncMPTClient)


@pytest.fixture
def operations_client() -> AsyncMock:
    return MagicMock(spec=AsyncMPTClient)

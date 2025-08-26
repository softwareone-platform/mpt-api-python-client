import pytest

from mpt_api_client.http.service import AsyncServiceBase, SyncServiceBase
from tests.conftest import DummyModel


class DummyService(SyncServiceBase[DummyModel]):
    _endpoint = "/api/v1/test"
    _model_class = DummyModel


class AsyncDummyService(AsyncServiceBase[DummyModel]):
    _endpoint = "/api/v1/test"
    _model_class = DummyModel


@pytest.fixture
def dummy_service(http_client) -> DummyService:
    return DummyService(http_client=http_client)


@pytest.fixture
def async_dummy_service(async_http_client) -> AsyncDummyService:
    return AsyncDummyService(http_client=async_http_client)

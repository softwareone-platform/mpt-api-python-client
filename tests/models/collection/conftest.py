import pytest

from mpt_api_client.models import Collection
from tests.conftest import DummyModel


@pytest.fixture
def response_collection_data():
    return [
        {"id": 1, "user": {"name": "Alice", "surname": "Smith"}, "status": "active"},
        {"id": 2, "user": {"name": "Bob", "surname": "Johnson"}, "status": "inactive"},
        {"id": 3, "user": {"name": "Charlie", "surname": "Brown"}, "status": "active"},
    ]


@pytest.fixture
def empty_collection():
    return Collection()


@pytest.fixture
def collection_items(response_collection_data):
    return [DummyModel(resource_data) for resource_data in response_collection_data]


@pytest.fixture
def collection(collection_items):
    return Collection(collection_items)

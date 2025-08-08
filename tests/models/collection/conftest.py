import pytest

from mpt_api_client.models import Collection, Resource


@pytest.fixture
def meta_data():
    return {"pagination": {"limit": 10, "offset": 0, "total": 3}, "ignored": ["field1"]}


@pytest.fixture
def response_collection_data():
    return [
        {"id": 1, "user": {"name": "Alice", "surname": "Smith"}, "status": "active"},
        {"id": 2, "user": {"name": "Bob", "surname": "Johnson"}, "status": "inactive"},
        {"id": 3, "user": {"name": "Charlie", "surname": "Brown"}, "status": "active"},
    ]


TestCollection = Collection[Resource]


@pytest.fixture
def empty_collection():
    return TestCollection()


@pytest.fixture
def collection(response_collection_data):
    return TestCollection(response_collection_data)

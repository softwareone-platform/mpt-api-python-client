import pytest

from tests.models.collection.conftest import TestCollection


def test_iteration(collection):
    resources = list(collection)

    assert len(resources) == 3


def test_iteration_next(response_collection_data):
    collection = TestCollection(response_collection_data)

    iterator = iter(collection)
    assert next(iterator).id == response_collection_data[0]["id"]
    assert next(iterator).id == response_collection_data[1]["id"]
    assert next(iterator).id == response_collection_data[2]["id"]

    # Check that iterator is exhausted
    with pytest.raises(StopIteration):
        next(iterator)

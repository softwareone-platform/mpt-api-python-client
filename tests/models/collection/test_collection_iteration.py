import pytest


def test_iteration(collection):
    resources = list(collection)

    assert len(resources) == 3


def test_iteration_next(collection, response_collection_data):
    iterator = iter(collection)
    assert next(iterator).to_dict() == response_collection_data[0]
    assert next(iterator).to_dict() == response_collection_data[1]
    assert next(iterator).to_dict() == response_collection_data[2]

    # Check that iterator is exhausted
    with pytest.raises(StopIteration):
        next(iterator)

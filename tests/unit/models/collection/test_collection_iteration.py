import pytest


def test_iteration(collection):
    result = list(collection)

    assert len(result) == 3


def test_iteration_next(collection, response_collection_data):
    result = iter(collection)

    assert next(result).to_dict() == response_collection_data[0]
    assert next(result).to_dict() == response_collection_data[1]
    assert next(result).to_dict() == response_collection_data[2]
    # Check that iterator is exhausted
    with pytest.raises(StopIteration):
        next(result)

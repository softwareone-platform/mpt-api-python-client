import pytest


def test_getitem_access(collection, response_collection_data):
    assert collection[0].to_dict() == response_collection_data[0]
    assert collection[1].to_dict() == response_collection_data[1]
    assert collection[2].to_dict() == response_collection_data[2]


def test_getitem_out_of_bounds(collection):
    with pytest.raises(IndexError):
        collection[10]


def test_length(empty_collection, collection):
    assert len(empty_collection) == 0
    assert len(collection) == 3


def test_bool_conversion(empty_collection, collection, response_collection_data):
    assert bool(empty_collection) is False
    assert bool(collection) is True


def test_to_list_method(collection, response_collection_data):
    resources = collection.to_list()

    assert resources == response_collection_data
    assert isinstance(resources, list)


def test_empty_collection_to_list(empty_collection):
    resources = empty_collection.to_list()

    assert resources == []
    assert isinstance(resources, list)

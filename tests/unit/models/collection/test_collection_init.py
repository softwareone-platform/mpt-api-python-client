def test_generic_collection_empty(empty_collection):  # noqa: AAA01
    assert empty_collection.meta is None
    assert len(empty_collection) == 0
    assert list(empty_collection) == []
    assert not empty_collection


def test_generic_collection_with_data(collection):  # noqa: AAA01
    assert len(collection) == 3
    assert bool(collection) is True
    for resource in collection.to_list():
        assert isinstance(resource, dict)

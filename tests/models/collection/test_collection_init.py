import pytest
from httpx import Response

from mpt_api_client.models.collection import Collection
from mpt_api_client.models.meta import Meta
from tests.models.collection.conftest import TestCollection


def test_generic_collection_empty(empty_collection):
    assert empty_collection.meta is None
    assert len(empty_collection) == 0
    assert list(empty_collection) == []
    assert not empty_collection


def test_generic_collection_with_data(collection, response_collection_data):
    assert len(collection) == 3
    assert bool(collection) is True
    assert collection.to_list() == response_collection_data


def test_from_response(meta_data, response_collection_data):
    response = Response(200, json={"data": response_collection_data, "$meta": meta_data})
    expected_meta = Meta.from_response(response)

    collection = TestCollection.from_response(response)

    assert collection.to_list() == response_collection_data
    assert collection.meta == expected_meta
    assert len(collection) == 3


def test_wrong_data_type_from_response():
    response = Response(200, json={"data": {"not": "a list"}})

    with pytest.raises(
        TypeError, match=r"Response `data` must be a list for collection endpoints."
    ):
        Collection.from_response(response)


def test_collection_with_meta(meta_data, response_collection_data):
    response = Response(200, json={"data": response_collection_data, "$meta": meta_data})
    meta = Meta.from_response(response)

    collection = TestCollection.from_response(response)

    assert collection.meta == meta

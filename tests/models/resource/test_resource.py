import pytest
from httpx import Response

from mpt_api_client.models import Meta, Resource


@pytest.fixture
def meta_data():
    return {"pagination": {"limit": 10, "offset": 20, "total": 100}, "ignored": ["one"]}  # noqa: WPS226


def test_resource_empty():
    resource = Resource()

    assert resource.meta is None
    assert resource.to_dict() == {}


def test_from_response(meta_data):
    record_data = {"id": 1, "name": {"given": "Albert", "family": "Einstein"}}
    response = Response(200, json={"data": record_data, "$meta": meta_data})
    expected_meta = Meta.from_response(response)

    resource = Resource.from_response(response)

    assert resource.to_dict() == record_data
    assert resource.meta == expected_meta


def test_attribute_getter(mocker, meta_data):
    resource_data = {"id": 1, "name": {"given": "Albert", "family": "Einstein"}}
    response = Response(200, json={"data": resource_data, "$meta": meta_data})

    resource = Resource.from_response(response)

    assert resource.id == 1
    assert resource.name.given == "Albert"


def test_attribute_setter():
    resource_data = {"id": 1, "name": {"given": "Albert", "family": "Einstein"}}
    resource = Resource(resource_data)

    resource.id = 2
    resource.name.given = "John"

    assert resource.id == 2
    assert resource.name.given == "John"


def test_wrong_data_type():
    with pytest.raises(TypeError, match=r"Response data must be a dict."):
        Resource.from_response(Response(200, json={"data": 1}))

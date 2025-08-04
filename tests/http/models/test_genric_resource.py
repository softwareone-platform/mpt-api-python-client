import pytest
from httpx import Response

from mpt_api_client.http.models import GenericResource, Meta


@pytest.fixture
def meta_data():
    return {"pagination": {"limit": 10, "offset": 20, "total": 100}, "ignored": ["one"]}  # noqa: WPS226


def test_generic_resource_empty():
    resource = GenericResource()
    assert resource.meta is None
    assert resource.to_dict() == {}


def test_from_response(meta_data):
    record_data = {"id": 1, "name": {"given": "Albert", "family": "Einstein"}}
    response = Response(200, json={"data": record_data, "$meta": meta_data})
    expected_meta = Meta.from_response(response)

    resource = GenericResource.from_response(response)

    assert resource.to_dict() == record_data
    assert resource.meta == expected_meta


def test_attribute_access():
    resource_data = {"id": 1, "name": {"given": "Albert", "family": "Einstein"}}
    meta = Meta.from_response(Response(200, json={"$meta": {}}))
    resource = GenericResource(resource_data=resource_data, meta=meta)

    assert resource.meta == meta

    assert resource.id == 1

    with pytest.raises(AttributeError, match=r"'Box' object has no attribute 'address'"):
        resource.address  # noqa: B018

    with pytest.raises(AttributeError, match=r"'Box' object has no attribute 'surname'"):
        resource.name.surname  # noqa: B018

    assert resource.name.given == "Albert"
    assert resource.name.to_dict() == resource_data["name"]


def test_attribute_setter():
    resource_data = {"id": 1, "name": {"given": "Albert", "family": "Einstein"}}
    resource = GenericResource(resource_data)

    resource.id = 2
    assert resource.id == 2

    resource.name.given = "John"
    assert resource.name.given == "John"


def test_wrong_data_type():
    with pytest.raises(TypeError, match=r"Response data must be a dict."):
        GenericResource.from_response(Response(200, json={"data": 1}))

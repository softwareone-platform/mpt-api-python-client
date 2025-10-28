import pytest
from httpx import Response

from mpt_api_client.models import Meta, Model


@pytest.fixture
def meta_data():
    return {"pagination": {"limit": 10, "offset": 20, "total": 100}, "ignored": ["one"]}  # noqa: WPS226


def test_resource_empty():
    resource = Model()

    assert resource.meta is None
    assert resource.to_dict() == {}


def test_from_response(meta_data):
    record_data = {"id": 1, "name": {"given": "Albert", "family": "Einstein"}}
    response = Response(200, json=record_data | {"$meta": meta_data})
    expected_meta = Meta.from_response(response)

    resource = Model.from_response(response)

    assert resource.to_dict() == record_data
    assert resource.meta == expected_meta


def test_attribute_getter(mocker, meta_data):
    resource_data = {"id": 1, "name": {"given": "Albert", "family": "Einstein"}}
    response_data = resource_data | {"$meta": meta_data}

    response = Response(200, json=response_data)

    resource = Model.from_response(response)

    assert resource.id == "1"
    assert resource.name.given == "Albert"


def test_attribute_setter():
    resource_data = {"id": 1, "name": {"given": "Albert", "family": "Einstein"}}
    resource = Model(resource_data)

    resource.id = "2"
    resource.name.given = "John"

    assert resource.id == "2"
    assert resource.name.given == "John"


def test_wrong_data_type():
    response = Response(200, json=1)
    with pytest.raises(TypeError, match=r"Response data must be a dict."):
        Model.from_response(response)


def test_id_property_with_string_id():
    resource_data = {"id": "abc-123"}
    resource = Model(resource_data)

    assert resource.id == "abc-123"
    assert isinstance(resource.id, str)


def test_id_property_with_numeric_id():
    resource_data = {"id": 1024}
    resource = Model(resource_data)

    assert resource.id == "1024"
    assert isinstance(resource.id, str)

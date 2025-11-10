from typing import ClassVar

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


def test_case_conversion():
    resource_data = {"id": "abc-123", "FullName": "Alice Smith"}

    resource = Model(resource_data)

    assert resource.full_name == "Alice Smith"
    assert resource.to_dict() == resource_data
    with pytest.raises(AttributeError):
        _ = resource.FullName  # noqa: WPS122


def test_deep_case_conversion():
    resource_data = {"id": "ABC-123", "contact": {"id": "ABC-345", "FullName": "Alice Smith"}}
    expected_resource_data = {
        "id": "ABC-123",
        "contact": {"id": "ABC-345", "FullName": "Alice Smith", "StreetAddress": "123 Main St"},
    }

    resource = Model(resource_data)
    resource.contact.StreetAddress = "123 Main St"

    assert resource.contact.full_name == "Alice Smith"
    assert resource.contact.street_address == "123 Main St"
    assert resource.to_dict() == expected_resource_data

    with pytest.raises(AttributeError):
        _ = resource.contact.FullName  # noqa: WPS122

    with pytest.raises(AttributeError):
        _ = resource.contact.StreetAddress  # noqa: WPS122


def test_repr():
    resource_data = {"id": "abc-123", "FullName": "Alice Smith"}

    resource = Model(resource_data)

    assert repr(resource) == "<Model abc-123>"
    assert str(resource) == "<Model abc-123>"


def test_mapping():
    class MappingModel(Model):  # noqa: WPS431
        _attribute_mapping: ClassVar[dict[str, str]] = {
            "second_id": "resource_id",
            "Full_Name": "name",
        }

    resource_data = {"id": "abc-123", "second_id": "resource-abc-123", "Full_Name": "Alice Smith"}

    resource = MappingModel(resource_data)

    assert resource.name == "Alice Smith"
    assert resource.resource_id == "resource-abc-123"
    assert resource.to_dict() == resource_data

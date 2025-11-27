from typing import ClassVar

import pytest
from httpx import Response

from mpt_api_client.models import Meta, Model


@pytest.fixture
def meta_data():
    return {"pagination": {"limit": 10, "offset": 20, "total": 100}, "ignored": ["one"]}  # noqa: WPS226


def test_resource_empty():
    result = Model()

    assert result.meta is None
    assert result.to_dict() == {}


def test_from_response(meta_data):
    record_data = {"id": 1, "name": {"given": "Albert", "family": "Einstein"}}
    response = Response(200, json=record_data | {"$meta": meta_data})
    expected_meta = Meta.from_response(response)

    result = Model.from_response(response)

    assert result.to_dict() == record_data
    assert result.meta == expected_meta


def test_attribute_getter(meta_data):
    resource_data = {"id": 1, "name": {"given": "Albert", "family": "Einstein"}}
    response_data = resource_data | {"$meta": meta_data}
    response = Response(200, json=response_data)

    result = Model.from_response(response)

    assert result.id == "1"
    assert result.name.given == "Albert"


def test_attribute_setter():  # noqa: AAA01
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

    result = Model(resource_data)

    assert result.id == "abc-123"
    assert isinstance(result.id, str)


def test_id_property_with_numeric_id():
    resource_data = {"id": 1024}

    result = Model(resource_data)

    assert result.id == "1024"
    assert isinstance(result.id, str)


def test_case_conversion():
    resource_data = {"id": "abc-123", "FullName": "Alice Smith"}

    result = Model(resource_data)

    assert result.full_name == "Alice Smith"
    assert result.to_dict() == resource_data
    with pytest.raises(AttributeError):
        _ = result.FullName  # noqa: WPS122


def test_deep_case_conversion():
    resource_data = {"id": "ABC-123", "contact": {"id": "ABC-345", "FullName": "Alice Smith"}}
    expected_resource_data = {
        "id": "ABC-123",
        "contact": {"id": "ABC-345", "FullName": "Alice Smith", "StreetAddress": "123 Main St"},
    }
    resource = Model(resource_data)

    resource.contact.StreetAddress = "123 Main St"  # act

    assert resource.contact.full_name == "Alice Smith"
    assert resource.contact.street_address == "123 Main St"
    assert resource.to_dict() == expected_resource_data
    with pytest.raises(AttributeError):
        _ = resource.contact.FullName  # noqa: WPS122
    with pytest.raises(AttributeError):
        _ = resource.contact.StreetAddress  # noqa: WPS122


def test_repr():
    resource_data = {"id": "abc-123", "FullName": "Alice Smith"}

    result = Model(resource_data)

    assert repr(result) == "<Model abc-123>"
    assert str(result) == "<Model abc-123>"


def test_mapping():
    class MappingModel(Model):  # noqa: WPS431
        _attribute_mapping: ClassVar[dict[str, str]] = {
            "second_id": "resource_id",
            "Full_Name": "name",
        }

    # BL
    resource_data = {"id": "abc-123", "second_id": "resource-abc-123", "Full_Name": "Alice Smith"}

    result = MappingModel(resource_data)

    assert result.name == "Alice Smith"
    assert result.resource_id == "resource-abc-123"
    assert result.to_dict() == resource_data

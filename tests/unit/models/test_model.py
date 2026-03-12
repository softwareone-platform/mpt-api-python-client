import pytest
from httpx import Response

from mpt_api_client.models import Meta, Model
from mpt_api_client.models.model import BaseModel, ModelList, to_snake_case  # noqa: WPS347


class AgreementDummy(Model):  # noqa: WPS431
    """Dummy class for testing."""


class ContactDummy(Model):
    """Dummy class for testing."""

    name: str


class AgreementWithContactDummy(Model):
    """Dummy class for testing."""

    contact: ContactDummy


class TypedListItemDummy(BaseModel):
    """Dummy item for typed list tests."""

    name: str


class TypedListContainerDummy(BaseModel):
    """Dummy container with a typed list field."""

    entries: list[TypedListItemDummy]


class DictTypedContainerDummy(BaseModel):
    """Dummy container with a dict-typed field."""

    metadata: dict[str, str]


class ScalarListContainerDummy(BaseModel):
    """Dummy container with a list[str] field."""

    tags: list[str]


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


def test_attribute_id(meta_data):
    resource_data = {"id": "1", "name": {"given": "Albert", "family": "Einstein"}}
    response_data = resource_data | {"$meta": meta_data}
    response = Response(200, json=response_data)
    resource = Model.from_response(response)

    resource.id = "R-1"  # act

    assert resource.id == "R-1"
    assert resource.name.given == "Albert"
    assert resource.to_dict() == {"id": "R-1", "name": {"given": "Albert", "family": "Einstein"}}


def test_wrong_data_type():
    response = Response(200, json=1)

    with pytest.raises(TypeError, match=r"Response data must be a dict."):
        Model.from_response(response)


def test_id_property_with_string_id():
    resource_data = {"id": "abc-123"}

    result = Model(resource_data)

    assert result.id == "abc-123"
    assert isinstance(result.id, str)


def test_case_conversion():
    resource_data = {"id": "abc-123", "FullName": "Alice Smith"}

    result = Model(resource_data)

    assert result.full_name == "Alice Smith"
    assert result.to_dict() == {"id": "abc-123", "fullName": "Alice Smith"}
    with pytest.raises(AttributeError):
        _ = result.FullName  # noqa: WPS122


def test_deep_case_conversion():
    resource_data = {"id": "ABC-123", "contact": {"id": "ABC-345", "FullName": "Alice Smith"}}
    expected_resource_data = {
        "id": "ABC-123",
        "contact": {"id": "ABC-345", "fullName": "Alice Smith", "streetAddress": "123 Main St"},
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
    resource_data = {"id": "abc-123", "secondId": "resource-abc-123", "fullName": "Alice Smith"}

    result = Model(**resource_data)

    assert result.full_name == "Alice Smith"
    assert result.second_id == "resource-abc-123"
    assert result.to_dict() == resource_data


def test_overwritting():
    agreement_data = {
        "id": "AGR-123",
        "parameters": {
            "ordering": [
                {"externalId": "contact", "value": "Hommer Simpson"},
                {"externalId": "address", "value": "Springfield"},
            ]
        },
    }
    agreement = AgreementDummy(agreement_data)

    agreement.parameters.ordering[1] = {"externalId": "address", "value": "Springfield"}  # act

    assert agreement.id == "AGR-123"
    assert agreement.parameters.ordering[0].external_id == "contact"
    assert agreement.to_dict() == agreement_data


def test_append():
    agreement_data = {
        "id": "AGR-123",
        "parameters": {
            "ordering": [
                {"externalId": "contact", "value": "Hommer Simpson"},
                {"externalId": "address", "value": "Springfield"},
            ]
        },
    }
    agreement = AgreementDummy(agreement_data)
    new_param = {"externalId": "email", "value": "homer.simpson@example.com"}

    agreement.parameters.ordering.append(new_param)  # act

    assert agreement.id == "AGR-123"
    assert [agr_param.external_id for agr_param in agreement.parameters.ordering] == [
        "contact",
        "address",
        "email",
    ]
    agreement_data["parameters"]["ordering"].append(new_param)
    assert agreement.to_dict() == agreement_data


def test_overwrite_list():
    ordering_parameters = [
        {"externalId": "contact", "value": "Hommer Simpson"},
        {"externalId": "address", "value": "Springfield"},
    ]
    agreement_data = {
        "id": "AGR-123",
        "parameters": {"ordering": ordering_parameters},
    }
    agreement = AgreementDummy(agreement_data)

    agreement.parameters.ordering = ordering_parameters  # act

    assert agreement.id == "AGR-123"
    assert [agr_param.external_id for agr_param in agreement.parameters.ordering] == [
        "contact",
        "address",
    ]
    assert agreement.to_dict() == agreement_data


def test_advanced_mapping():
    ordering_parameters = [
        {"externalId": "contact", "value": "Hommer Simpson"},
        {"externalId": "address", "value": "Springfield"},
    ]
    agreement_data = {
        "id": "AGR-123",
        "contact": {"name": "Hommer Simpson"},
        "parameters": {"ordering": ordering_parameters},
    }
    agreement = AgreementWithContactDummy(agreement_data)

    agreement.parameters.ordering = ordering_parameters  # act

    assert isinstance(agreement.contact, ContactDummy)
    assert [agr_param.external_id for agr_param in agreement.parameters.ordering] == [
        "contact",
        "address",
    ]
    assert agreement.to_dict() == agreement_data


def test_to_snake_case_already_snake():
    result = to_snake_case("already_snake")  # act

    assert result == "already_snake"


def test_model_list_extend():
    ml = ModelList([{"id": "1"}])

    ml.extend([{"id": "2"}, {"id": "3"}])  # act

    assert [ml_item.id for ml_item in ml] == ["1", "2", "3"]


def test_model_list_insert():
    ml = ModelList([{"id": "1"}, {"id": "3"}])

    ml.insert(1, {"id": "2"})  # act

    assert [ml_item.id for ml_item in ml] == ["1", "2", "3"]


def test_model_list_process_item_nested_list():
    nested = [{"id": "a"}, {"id": "b"}]

    ml = ModelList([nested])  # act

    assert isinstance(ml[0], ModelList)
    assert ml[0][0].id == "a"


def test_model_list_process_item_scalar():
    ml = ModelList(["a", "b", "c"])  # act

    assert ml == ["a", "b", "c"]


def test_base_model_getattr_from_dict():
    model = BaseModel(foo="bar")

    result = model.__getattr__("foo")  # noqa: PLC2801

    assert result == "bar"


def test_base_model_setattr_private():
    model = BaseModel(foo="bar")

    model._private = "secret"  # noqa: SLF001  # act

    assert model._private == "secret"  # noqa: SLF001


def test_to_dict_excludes_private_attrs():
    model = BaseModel(foo="bar")
    model._private = "secret"  # noqa: SLF001

    result = model.to_dict()

    assert result == {"foo": "bar"}
    assert "_private" not in result


def test_process_value_typed_list():
    container = TypedListContainerDummy(entries=[{"name": "one"}, {"name": "two"}])  # act

    assert all(isinstance(entry, TypedListItemDummy) for entry in container.entries)
    assert [entry.name for entry in container.entries] == ["one", "two"]


def test_process_value_existing_base_model():
    nested = BaseModel(value="test")
    model = BaseModel()

    model.nested = nested  # act

    assert model.nested is nested


def test_process_value_non_list_target():
    container = DictTypedContainerDummy()

    container.metadata = [{"id": "1"}]  # act

    assert isinstance(container.metadata, ModelList)
    assert container.metadata[0].id == "1"


def test_process_value_scalar_list_elements():
    container = ScalarListContainerDummy(tags=["a", "b", "c"])  # act

    assert isinstance(container.tags, ModelList)
    assert list(container.tags) == ["a", "b", "c"]

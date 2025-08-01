import re

import pytest
from httpx import Response

from mpt_api_client.http.models import GenericResource, Meta


@pytest.fixture
def meta_data():
    return {"pagination": {"limit": 10, "offset": 20, "total": 100}, "ignored": ["one"]}  # noqa: WPS226


class TestGenericResource:  # noqa: WPS214
    def test_generic_resource_empty(self):
        resource = GenericResource()
        with pytest.raises(AttributeError):
            _ = resource._meta

    def test_initialization_with_data(self):
        resource = GenericResource(name="test", value=123)

        assert resource.name == "test"
        assert resource.value == 123

    def test_init(self, meta_data):
        resource = {"$meta": meta_data, "key": "value"}  # noqa: WPS445 WPS517
        init_one = GenericResource(resource)
        init_two = GenericResource(**resource)
        assert init_one == init_two

    def test_generic_resource_meta_property_with_data(self, meta_data):
        resource = GenericResource({"$meta": meta_data})
        assert resource._meta == Meta(**meta_data)

    def test_generic_resource_box_functionality(self):
        resource = GenericResource(id=1, name="test_resource", nested={"key": "value"})

        assert resource.id == 1
        assert resource.name == "test_resource"
        assert resource.nested.key == "value"

    def test_with_both_meta_and_response(self, meta_data):
        response = Response(200, json={})
        meta_data["response"] = response
        meta_object = Meta(**meta_data)

        resource = GenericResource(
            data="test_data",
            **{"$meta": meta_data},  # noqa: WPS445 WPS517
        )

        assert resource.data == "test_data"
        assert resource._meta == meta_object

    def test_dynamic_attribute_access(self):
        resource = GenericResource()

        resource.dynamic_field = "dynamic_value"
        resource.nested_object = {"inner": "data"}

        assert resource.dynamic_field == "dynamic_value"
        assert resource.nested_object.inner == "data"


class TestGenericResourceFromResponse:
    @pytest.fixture
    def meta_data_single(self):
        return {"ignored": ["one"]}  # noqa: WPS226

    @pytest.fixture
    def meta_data_two_resources(self):
        return {"pagination": {"limit": 10, "offset": 0, "total": 2}, "ignored": ["one"]}  # noqa: WPS226

    @pytest.fixture
    def meta_data_multiple(self):
        return {"ignored": ["one", "two"]}  # noqa: WPS226

    @pytest.fixture
    def single_resource_data(self):
        return {"id": 1, "name": "test"}

    @pytest.fixture
    def single_resource_response(self, single_resource_data, meta_data_single):
        return Response(200, json={"data": single_resource_data, "$meta": meta_data_single})

    @pytest.fixture
    def multiple_resource_response(self, single_resource_data, meta_data_two_resources):
        return Response(
            200,
            json={
                "data": [single_resource_data, single_resource_data],
                "$meta": meta_data_two_resources,
            },
        )

    def test_malformed_meta_response(self):
        with pytest.raises(TypeError, match=re.escape("Response $meta must be a dict.")):
            _resource = GenericResource.from_response(Response(200, json={"data": {}, "$meta": 4}))

    def test_single_resource(self, single_resource_response):
        resource = GenericResource.from_response(single_resource_response)
        assert resource.id == 1
        assert resource.name == "test"
        assert isinstance(resource._meta, Meta)
        assert resource._meta.response == single_resource_response

    def test_two_resources(self, multiple_resource_response, single_resource_data):
        with pytest.raises(TypeError, match=r"Response data must be a dict."):
            _resource = GenericResource.from_response(multiple_resource_response)

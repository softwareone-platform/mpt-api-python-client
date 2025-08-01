import pytest
from httpx import Response

from mpt_api_client.http.models import Meta, Pagination


class TestMeta:

    @pytest.fixture
    def responses_fixture(self):
        response_data = {
            "$meta": {
                "ignored": ["ignored"],
                "pagination": {"limit": 25, "offset": 50, "total": 300}

            }
        }
        return Response(status_code=200, json=response_data)

    @pytest.fixture
    def invalid_response_fixture(self):
        response_data = {
            "$meta": "invalid_meta"
        }
        return Response(status_code=200, json=response_data)

    def test_meta_initialization_empty(self):
        meta = Meta()
        assert meta.pagination == Pagination(limit=0, offset=0, total=0)

    def test_meta_from_response(self, responses_fixture):
        meta = Meta.from_response(responses_fixture)

        assert isinstance(meta.pagination, Pagination)
        assert meta.pagination.limit == 25
        assert meta.pagination.offset == 50
        assert meta.pagination.total == 300

    def test_invalid_meta_from_response(self, invalid_response_fixture):
        with pytest.raises(TypeError):
            Meta.from_response(invalid_response_fixture)

    def test_meta_with_pagination_object(self):
        pagination = Pagination(limit=10, offset=0, total=100)
        meta = Meta(pagination=pagination)

        assert meta.pagination == Pagination(limit=10, offset=0, total=100)

import pytest
from httpx import Response

from mpt_api_client.models import Meta, Pagination


@pytest.fixture
def responses_fixture():
    response_data = {
        "$meta": {
            "ignored": ["ignored"],
            "pagination": {"limit": 25, "offset": 50, "total": 300},
        }
    }
    return Response(status_code=200, json=response_data)


@pytest.fixture
def invalid_response_fixture():
    response_data = {"$meta": "invalid_meta"}
    return Response(status_code=200, json=response_data)


def test_meta_from_response(responses_fixture):
    result = Meta.from_response(responses_fixture)

    assert isinstance(result.pagination, Pagination)
    assert result.pagination == Pagination(limit=25, offset=50, total=300)


def test_invalid_meta_from_response(invalid_response_fixture):
    with pytest.raises(TypeError, match=r"Response \$meta must be a dict."):
        Meta.from_response(invalid_response_fixture)

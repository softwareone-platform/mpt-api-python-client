import pytest
from httpx import Response

from mpt_api_client.models import Meta, Pagination


@pytest.fixture
def responses_fixture():
    response_data = {
        "$meta": {
            "omitted": ["externalIds", "price"],
            "pagination": {"limit": 25, "offset": 50, "total": 300},
        }
    }
    return Response(status_code=200, json=response_data)


@pytest.fixture
def pagination_only_response_fixture():
    response_data = {"$meta": {"pagination": {"limit": 25, "offset": 50, "total": 300}}}
    return Response(status_code=200, json=response_data)


@pytest.fixture
def legacy_ignored_response_fixture():
    # The key the client used to read. The API has never sent it, so it must not
    # populate `omitted` now that the correct key is parsed.
    response_data = {"$meta": {"ignored": ["externalIds"]}}
    return Response(status_code=200, json=response_data)


@pytest.fixture
def invalid_response_fixture():
    response_data = {"$meta": "invalid_meta"}
    return Response(status_code=200, json=response_data)


def test_meta_from_response(responses_fixture):
    result = Meta.from_response(responses_fixture)

    assert isinstance(result.pagination, Pagination)
    assert result.pagination == Pagination(limit=25, offset=50, total=300)
    assert result.omitted == ["externalIds", "price"]


def test_omitted_defaults_to_empty(pagination_only_response_fixture):
    result = Meta.from_response(pagination_only_response_fixture)

    assert result.omitted == []


def test_meta_ignores_the_legacy_ignored_member(legacy_ignored_response_fixture):
    result = Meta.from_response(legacy_ignored_response_fixture)

    assert result.omitted == []


def test_invalid_meta_from_response(invalid_response_fixture):
    with pytest.raises(TypeError, match=r"Response \$meta must be a dict."):
        Meta.from_response(invalid_response_fixture)

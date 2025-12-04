import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery
from tests.e2e.helper import assert_update_resource, create_fixture_resource_and_delete

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_authorization(authorizations_service, authorization_data):
    with create_fixture_resource_and_delete(
        authorizations_service, authorization_data
    ) as authorization:
        yield authorization


def test_get_authorization(authorizations_service, authorization_id):
    result = authorizations_service.get(authorization_id)

    assert result.id == authorization_id


def test_create_authorization(created_authorization, authorization_data):  # noqa: AAA01
    assert created_authorization.name == authorization_data["name"]


def test_filter_authorizations(authorizations_service, authorization_id):
    select_fields = ["-description"]
    filtered = authorizations_service.filter(RQLQuery(id=authorization_id)).select(*select_fields)

    result = list(filtered.iterate())

    assert len(result) == 1
    assert result[0].id == authorization_id


def test_get_authorization_not_found(authorizations_service):
    bogus_id = "AUT-0000-0000"

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        authorizations_service.get(bogus_id)


def test_update_authorization(authorizations_service, authorization_id, short_uuid):
    assert_update_resource(
        authorizations_service, authorization_id, "notes", f"e2e test - {short_uuid}"
    )  # act

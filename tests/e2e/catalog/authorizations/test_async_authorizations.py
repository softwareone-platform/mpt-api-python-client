import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery
from tests.e2e.helper import assert_async_update_resource, async_create_fixture_resource_and_delete

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def async_authorizations_service(async_mpt_ops):
    return async_mpt_ops.catalog.authorizations


@pytest.fixture
async def created_authorization(async_authorizations_service, authorization_data):
    async with async_create_fixture_resource_and_delete(
        async_authorizations_service, authorization_data
    ) as authorization:
        yield authorization


def test_create_authorization(created_authorization, authorization_data):  # noqa: AAA01
    assert created_authorization.name == authorization_data["name"]


async def test_get_authorization(async_authorizations_service, authorization_id):
    result = await async_authorizations_service.get(authorization_id)

    assert result.id == authorization_id


async def test_filter_authorizations(async_authorizations_service, authorization_id):
    select_fields = ["-description"]
    filtered = async_authorizations_service.filter(RQLQuery(id=authorization_id)).select(
        *select_fields
    )

    result = [auth async for auth in filtered.iterate()]

    assert len(result) == 1
    assert result[0].id == authorization_id


async def test_get_authorization_not_found(async_authorizations_service):
    bogus_id = "AUT-0000-0000"

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_authorizations_service.get(bogus_id)


async def test_update_authorization(async_authorizations_service, authorization_id, short_uuid):
    await assert_async_update_resource(
        async_authorizations_service, authorization_id, "notes", f"e2e test - {short_uuid}"
    )

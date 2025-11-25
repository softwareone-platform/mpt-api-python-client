import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def async_pricing_policies_service(async_mpt_ops):
    return async_mpt_ops.catalog.pricing_policies


@pytest.fixture
async def async_created_pricing_policy(async_pricing_policies_service, pricing_policy_data):
    policy = await async_pricing_policies_service.create(pricing_policy_data)

    yield policy

    try:
        await async_pricing_policies_service.delete(policy.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete pricing policy {policy.id}: {error.title}")


def test_create_pricing_policy(async_created_pricing_policy, pricing_policy_data):
    assert async_created_pricing_policy.name == pricing_policy_data["name"]


async def test_get_pricing_policy(async_pricing_policies_service, async_created_pricing_policy):
    fetched = await async_pricing_policies_service.get(async_created_pricing_policy.id)
    assert fetched.id == async_created_pricing_policy.id


async def test_get_pricing_policy_by_id(
    async_pricing_policies_service, async_created_pricing_policy
):
    fetched = await async_pricing_policies_service.get(async_created_pricing_policy.id)
    assert fetched.id == async_created_pricing_policy.id


async def test_iterate_pricing_policies(
    async_pricing_policies_service, async_created_pricing_policy
):
    policies = [policy async for policy in async_pricing_policies_service.iterate()]
    assert any(policy.id == async_created_pricing_policy.id for policy in policies)


async def test_filter_pricing_policies(
    async_pricing_policies_service, async_created_pricing_policy
):
    target_id = async_created_pricing_policy.id
    select_fields = ["-description"]
    filtered = async_pricing_policies_service.filter(RQLQuery(id=target_id)).select(*select_fields)
    policies = [policy async for policy in filtered.iterate()]
    assert len(policies) == 1
    assert policies[0].id == target_id


async def test_activate_deactivate_pricing_policy(
    async_pricing_policies_service, async_created_pricing_policy
):
    deactivate = await async_pricing_policies_service.disable(async_created_pricing_policy.id)
    assert deactivate.id == async_created_pricing_policy.id

    activated = await async_pricing_policies_service.activate(async_created_pricing_policy.id)
    assert activated.id == async_created_pricing_policy.id


async def test_delete_pricing_policy(async_pricing_policies_service, async_created_pricing_policy):
    await async_pricing_policies_service.delete(async_created_pricing_policy.id)  # act


async def test_get_pricing_policy_not_found(async_pricing_policies_service):
    bogus_id = "PPY-0000-NOTFOUND"
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_pricing_policies_service.get(bogus_id)


async def test_create_pricing_policy_invalid_data(async_pricing_policies_service):
    invalid_data = {"name": "e2e - delete me", "description": "invalid data"}
    with pytest.raises(MPTAPIError, match=r"400 One or more validation errors occurred"):
        await async_pricing_policies_service.create(invalid_data)

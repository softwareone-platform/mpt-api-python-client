import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def created_cloud_tenant(async_mpt_ops, cloud_tenant):
    new_cloud_tenant_request_data = cloud_tenant(name="E2E Created Cloud Tenant")

    new_cloud_tenant = await async_mpt_ops.accounts.cloud_tenants.create(new_cloud_tenant_request_data)

    yield new_cloud_tenant

    try:
        await async_mpt_ops.accounts.cloud_tenants.delete(new_cloud_tenant.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete cloud tenant: {error.title}")  # noqa: WPS421


async def test_get_cloud_tenant_by_id(async_mpt_ops, cloud_tenant_id):
    cloud_tenant = await async_mpt_ops.accounts.cloud_tenants.get(cloud_tenant_id)
    assert cloud_tenant is not None


async def test_list_cloud_tenants(async_mpt_ops):
    limit = 10
    cloud_tenants = await async_mpt_ops.accounts.cloud_tenants.fetch_page(limit=limit)
    assert len(cloud_tenants) > 0


async def test_get_cloud_tenant_by_id_not_found(async_mpt_ops, invalid_cloud_tenant_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.cloud_tenants.get(invalid_cloud_tenant_id)


async def test_filter_cloud_tenants(async_mpt_ops, cloud_tenant_id):
    select_fields = ["-name"]

    filtered_cloud_tenants = (
        await async_mpt_ops.accounts.cloud_tenants.filter(RQLQuery(id=cloud_tenant_id))
        .filter(RQLQuery(name="E2E Seeded Cloud Tenant"))
        .select(*select_fields)
    )

    cloud_tenants = list(filtered_cloud_tenants.iterate())

    assert len(cloud_tenants) == 1


def test_create_cloud_tenant(created_cloud_tenant):
    new_cloud_tenant = created_cloud_tenant
    assert new_cloud_tenant is not None


async def test_delete_cloud_tenant(async_mpt_ops, created_cloud_tenant):
    await async_mpt_ops.accounts.cloud_tenants.delete(created_cloud_tenant.id)


async def test_delete_cloud_tenant_not_found(async_mpt_ops, invalid_cloud_tenant_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.cloud_tenants.delete(invalid_cloud_tenant_id)


async def test_update_cloud_tenant(async_mpt_ops, cloud_tenant, created_cloud_tenant):
    updated_cloud_tenant_data = cloud_tenant(name="E2E Updated Cloud Tenant")

    updated_cloud_tenant = await async_mpt_ops.accounts.cloud_tenants.update(
        created_cloud_tenant.id, updated_cloud_tenant_data
    )

    assert updated_cloud_tenant is not None


async def test_update_cloud_tenant_not_found(async_mpt_ops, cloud_tenant, invalid_cloud_tenant_id):
    updated_cloud_tenant_data = cloud_tenant(name="Nonexistent Cloud Tenant")

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.cloud_tenants.update(invalid_cloud_tenant_id, updated_cloud_tenant_data)

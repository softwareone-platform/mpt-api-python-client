import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def created_user_group(async_mpt_ops, user_group):
    new_user_group_request_data = user_group()
    created_user_group = await async_mpt_ops.accounts.user_groups.create(
        new_user_group_request_data
    )

    yield created_user_group

    try:
        await async_mpt_ops.accounts.user_groups.delete(created_user_group.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete user group: {error.title}")  # noqa: WPS421


async def test_get_user_group_by_id(async_mpt_ops, user_group_id):
    user_group = await async_mpt_ops.accounts.user_groups.get(user_group_id)
    assert user_group is not None


async def test_list_user_groups(async_mpt_ops):
    limit = 10
    user_groups = await async_mpt_ops.accounts.user_groups.fetch_page(limit=limit)
    assert len(user_groups) > 0


async def test_get_user_group_by_id_not_found(async_mpt_ops, invalid_user_group_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.user_groups.get(invalid_user_group_id)


async def test_filter_user_groups(async_mpt_ops, user_group_id):
    select_fields = ["-name"]

    filtered_user_groups = (
        async_mpt_ops.accounts.user_groups.filter(RQLQuery(id=user_group_id))
        .filter(RQLQuery(name="E2E Seeded User Group"))
        .select(*select_fields)
    )

    user_groups = [
        filtered_user_group async for filtered_user_group in filtered_user_groups.iterate()
    ]

    assert len(user_groups) == 1


def test_create_user_group(created_user_group):
    new_user_group = created_user_group
    assert new_user_group is not None


async def test_delete_user_group(async_mpt_ops, created_user_group):
    await async_mpt_ops.accounts.user_groups.delete(created_user_group.id)


async def test_delete_user_group_not_found(async_mpt_ops, invalid_user_group_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.user_groups.delete(invalid_user_group_id)


async def test_update_user_group(async_mpt_ops, user_group, created_user_group):
    updated_user_group_data = user_group(name="E2E Updated User Group")

    updated_user_group = await async_mpt_ops.accounts.user_groups.update(
        created_user_group.id, updated_user_group_data
    )

    assert updated_user_group is not None


async def test_update_user_group_not_found(async_mpt_ops, user_group, invalid_user_group_id):
    updated_user_group_data = user_group(name="Nonexistent User Group")

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.user_groups.update(
            invalid_user_group_id, updated_user_group_data
        )

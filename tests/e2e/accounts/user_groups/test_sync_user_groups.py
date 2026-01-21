import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_user_group(mpt_ops, user_group_factory):
    """Fixture to create and yield a user group for testing."""
    new_user_group_request_data = user_group_factory()
    created_user_group = mpt_ops.accounts.user_groups.create(new_user_group_request_data)

    yield created_user_group

    try:
        mpt_ops.accounts.user_groups.delete(created_user_group.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete user group: {error.title}")  # noqa: WPS421


def test_get_user_group_by_id(mpt_ops, user_group_id):
    result = mpt_ops.accounts.user_groups.get(user_group_id)

    assert result is not None


def test_list_user_groups(mpt_ops):
    """Test listing user groups with a limit."""
    limit = 10

    result = mpt_ops.accounts.user_groups.fetch_page(limit=limit)

    assert len(result) > 0


def test_get_user_group_by_id_not_found(mpt_ops, invalid_user_group_id):
    """Test retrieving a user group by an invalid ID, expecting a 404 error."""
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_ops.accounts.user_groups.get(invalid_user_group_id)


def test_filter_user_groups(mpt_ops, user_group_id):
    """Test filtering user groups with specific criteria."""
    select_fields = ["-name"]
    filtered_user_groups = (
        mpt_ops.accounts.user_groups
        .filter(RQLQuery(id=user_group_id))
        .filter(RQLQuery(name="E2E Seeded User Group"))
        .select(*select_fields)
    )

    result = list(filtered_user_groups.iterate())

    assert len(result) == 1


def test_create_user_group(created_user_group):
    result = created_user_group

    assert result is not None


def test_delete_user_group(mpt_ops, created_user_group):
    mpt_ops.accounts.user_groups.delete(created_user_group.id)  # act


def test_delete_user_group_not_found(mpt_ops, invalid_user_group_id):
    """Test deleting a user group with an invalid ID, expecting a 404 error."""
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_ops.accounts.user_groups.delete(invalid_user_group_id)


def test_update_user_group(mpt_ops, user_group_factory, created_user_group):
    """Test updating a user group."""
    updated_user_group_data = user_group_factory(name="E2E Updated User Group")

    result = mpt_ops.accounts.user_groups.update(created_user_group.id, updated_user_group_data)

    assert result is not None


def test_update_user_group_not_found(mpt_ops, user_group_factory, invalid_user_group_id):
    """Test updating a user group with an invalid ID, expecting a 404 error."""
    updated_user_group_data = user_group_factory(name="Nonexistent User Group")

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_ops.accounts.user_groups.update(invalid_user_group_id, updated_user_group_data)

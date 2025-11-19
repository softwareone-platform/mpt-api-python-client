import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def created_api_token(async_mpt_vendor, api_token_factory):
    """Fixture to create and yield an asynchronous API token for testing."""
    new_api_token_request_data = api_token_factory()
    created_api_token = await async_mpt_vendor.accounts.api_tokens.create(
        new_api_token_request_data
    )

    yield created_api_token

    try:
        await async_mpt_vendor.accounts.api_tokens.delete(created_api_token.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete api token: {error.title}")  # noqa: WPS421


async def test_get_api_token_by_id(async_mpt_vendor, api_token_id):
    result = await async_mpt_vendor.accounts.api_tokens.get(api_token_id)

    assert result is not None


async def test_list_api_tokens(async_mpt_vendor):
    """Test listing API tokens with a limit."""
    limit = 10

    result = await async_mpt_vendor.accounts.api_tokens.fetch_page(limit=limit)

    assert len(result) > 0


async def test_get_api_token_by_id_not_found(async_mpt_vendor, invalid_api_token_id):
    """Test retrieving an API token by an invalid ID, expecting a 404 error."""
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_vendor.accounts.api_tokens.get(invalid_api_token_id)


async def test_filter_api_tokens(async_mpt_vendor, api_token_id):
    """Test filtering API tokens with specific criteria."""
    select_fields = ["-description"]
    filtered_api_tokens = (
        async_mpt_vendor.accounts.api_tokens.filter(RQLQuery(id=api_token_id))
        .filter(RQLQuery(name="E2E Seeded Token"))
        .select(*select_fields)
    )

    result = [filtered_api_token async for filtered_api_token in filtered_api_tokens.iterate()]

    assert len(result) == 1


def test_create_api_token(created_api_token):
    result = created_api_token

    assert result is not None


async def test_delete_api_token(async_mpt_vendor, created_api_token):
    await async_mpt_vendor.accounts.api_tokens.delete(created_api_token.id)  # act


async def test_delete_api_token_not_found(async_mpt_vendor, invalid_api_token_id):
    """Test deleting an API token with an invalid ID, expecting a 404 error."""
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_vendor.accounts.api_tokens.delete(invalid_api_token_id)


async def test_update_api_token(async_mpt_vendor, api_token_factory, created_api_token):
    """Test updating an API token."""
    updated_api_token_data = api_token_factory(name="E2E Updated API Token")

    result = await async_mpt_vendor.accounts.api_tokens.update(
        created_api_token.id, updated_api_token_data
    )

    assert result is not None


async def test_update_api_token_not_found(
    async_mpt_vendor, api_token_factory, invalid_api_token_id
):
    """Test updating an API token with an invalid ID, expecting a 404 error."""
    updated_api_token_data = api_token_factory(name="Nonexistent API Token")

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_vendor.accounts.api_tokens.update(
            invalid_api_token_id, updated_api_token_data
        )


async def test_api_token_disable(async_mpt_vendor, created_api_token):
    result = await async_mpt_vendor.accounts.api_tokens.disable(created_api_token.id)

    assert result is not None


async def test_api_token_disable_not_found(async_mpt_vendor, invalid_api_token_id):
    """Test disabling an API token with an invalid ID, expecting a 404 error."""
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_vendor.accounts.api_tokens.disable(invalid_api_token_id)


async def test_api_token_enable(async_mpt_vendor, created_api_token):
    """Test enabling an API token."""
    await async_mpt_vendor.accounts.api_tokens.disable(created_api_token.id)

    result = await async_mpt_vendor.accounts.api_tokens.enable(created_api_token.id)

    assert result is not None


async def test_api_token_enable_not_found(async_mpt_vendor, invalid_api_token_id):
    """Test enabling an API token with an invalid ID, expecting a 404 error."""
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_vendor.accounts.api_tokens.enable(invalid_api_token_id)

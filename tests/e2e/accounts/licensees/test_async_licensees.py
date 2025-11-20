import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def async_created_licensee(async_mpt_client, licensee_factory, account_icon):
    new_licensee_request_data = licensee_factory(name="E2E Created licensee")

    new_licensee = await async_mpt_client.accounts.licensees.create(
        new_licensee_request_data, logo=account_icon
    )

    yield new_licensee

    try:
        await async_mpt_client.accounts.licensees.delete(new_licensee.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete licensee: {error.title}")  # noqa: WPS421


async def test_get_licensee_by_id(async_mpt_client, licensee_id):
    licensee = await async_mpt_client.accounts.licensees.get(licensee_id)
    assert licensee is not None


async def test_list_licensees(async_mpt_client):
    limit = 10
    licensees = await async_mpt_client.accounts.licensees.fetch_page(limit=limit)
    assert len(licensees) > 0


async def test_get_licensee_by_id_not_found(async_mpt_client, invalid_licensee_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_client.accounts.licensees.get(invalid_licensee_id)


async def test_filter_licensees(async_mpt_client, licensee_id):
    select_fields = ["-address"]

    async_filtered_licensees = (
        async_mpt_client.accounts.licensees.filter(RQLQuery(id=licensee_id))
        .filter(RQLQuery(name="E2E Seeded Licensee"))
        .select(*select_fields)
    )

    licensees = [
        filtered_licensee async for filtered_licensee in async_filtered_licensees.iterate()
    ]

    assert len(licensees) == 1


def test_create_licensee(async_created_licensee):
    assert async_created_licensee is not None


async def test_delete_licensee(async_mpt_client, async_created_licensee):
    await async_mpt_client.accounts.licensees.delete(async_created_licensee.id)


async def test_delete_licensee_not_found(async_mpt_client, invalid_licensee_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_client.accounts.licensees.delete(invalid_licensee_id)


async def test_update_licensee(
    async_mpt_client, licensee_factory, account_icon, async_created_licensee
):
    updated_licensee_data = licensee_factory(name="E2E Updated Licensee")

    updated_licensee = await async_mpt_client.accounts.licensees.update(
        async_created_licensee.id, updated_licensee_data, logo=account_icon
    )

    assert updated_licensee is not None


async def test_update_licensee_not_found(
    async_mpt_client, licensee_factory, account_icon, invalid_licensee_id
):
    updated_licensee_data = licensee_factory(name="Nonexistent Licensee")

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_client.accounts.licensees.update(
            invalid_licensee_id, updated_licensee_data, logo=account_icon
        )


async def test_licensee_disable(async_mpt_client, async_created_licensee):
    disabled_licensee = await async_mpt_client.accounts.licensees.disable(async_created_licensee.id)

    assert disabled_licensee is not None


async def test_licensee_disable_not_found(async_mpt_client, invalid_licensee_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_client.accounts.licensees.disable(invalid_licensee_id)


async def test_licensee_enable(async_mpt_client, async_created_licensee):
    await async_mpt_client.accounts.licensees.disable(async_created_licensee.id)

    enabled_licensee = await async_mpt_client.accounts.licensees.enable(async_created_licensee.id)

    assert enabled_licensee is not None


async def test_licensee_enable_not_found(async_mpt_client, invalid_licensee_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_client.accounts.licensees.enable(invalid_licensee_id)

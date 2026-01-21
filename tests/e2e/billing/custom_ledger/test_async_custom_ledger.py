import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def created_custom_ledger(async_mpt_ops, custom_ledger_factory):
    new_custom_ledger_request_data = custom_ledger_factory()

    created_custom_ledger = await async_mpt_ops.billing.custom_ledgers.create(
        new_custom_ledger_request_data
    )

    yield created_custom_ledger

    try:
        await async_mpt_ops.billing.custom_ledgers.delete(created_custom_ledger.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete custom ledger: {error.title}")


async def test_get_custom_ledger_by_id(async_mpt_ops, custom_ledger_id):
    result = await async_mpt_ops.billing.custom_ledgers.get(custom_ledger_id)

    assert result is not None


async def test_list_custom_ledgers(async_mpt_ops):
    limit = 10

    result = await async_mpt_ops.billing.custom_ledgers.fetch_page(limit=limit)

    assert len(result) > 0


async def test_get_custom_ledger_by_id_not_found(async_mpt_ops, invalid_custom_ledger_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.billing.custom_ledgers.get(invalid_custom_ledger_id)


async def test_filter_custom_ledgers(async_mpt_ops, custom_ledger_id):
    select_fields = ["-price"]
    filtered_custom_ledgers = (
        async_mpt_ops.billing.custom_ledgers
        .filter(RQLQuery(id=custom_ledger_id))
        .filter(RQLQuery(name="E2E Seeded Custom Ledger"))
        .select(*select_fields)
    )

    result = [custom_ledger async for custom_ledger in filtered_custom_ledgers.iterate()]

    assert len(result) == 1


def test_create_custom_ledger(created_custom_ledger):
    result = created_custom_ledger

    assert result is not None


async def test_update_custom_ledger(async_mpt_ops, created_custom_ledger):
    name = "E2E Updated Custom Ledger"
    update_data = {
        "name": name,
    }

    result = await async_mpt_ops.billing.custom_ledgers.update(
        created_custom_ledger.id,
        update_data,
    )

    assert result is not None


async def test_delete_custom_ledger(async_mpt_ops, created_custom_ledger):
    result = created_custom_ledger

    await async_mpt_ops.billing.custom_ledgers.delete(result.id)


async def test_upload_custom_ledger(async_mpt_ops, created_custom_ledger, billing_custom_ledger_fd):
    result = await async_mpt_ops.billing.custom_ledgers.upload(
        custom_ledger_id=created_custom_ledger.id,
        file=billing_custom_ledger_fd,
    )

    assert result is not None

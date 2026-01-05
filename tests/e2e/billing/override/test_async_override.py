import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


async def test_get_billing_override_by_id(async_mpt_ops, billing_override_id):
    result = await async_mpt_ops.billing.manual_overrides.get(billing_override_id)

    assert result is not None


async def test_list_billing_overrides(async_mpt_ops):
    limit = 10

    result = await async_mpt_ops.billing.manual_overrides.fetch_page(limit=limit)

    assert len(result) > 0


async def test_get_billing_override_by_id_not_found(async_mpt_ops, invalid_billing_override_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.billing.manual_overrides.get(invalid_billing_override_id)


async def test_filter_billing_overrides(async_mpt_ops, billing_override_id):
    select_fields = ["-client"]
    filtered_billing_overrides = (
        async_mpt_ops.billing.manual_overrides.filter(RQLQuery(id=billing_override_id))
        .filter(RQLQuery(externalId="e2e-seeded-override"))
        .select(*select_fields)
    )

    result = [override async for override in filtered_billing_overrides.iterate()]

    assert len(result) == 1

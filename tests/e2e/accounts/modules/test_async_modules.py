import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery


async def test_get_module_by_id(async_mpt_ops, module_id):
    result = await async_mpt_ops.accounts.modules.get(module_id)

    assert result is not None


async def test_list_modules(async_mpt_ops):
    limit = 10

    result = await async_mpt_ops.accounts.modules.fetch_page(limit=limit)

    assert len(result) > 0


async def test_get_module_by_id_not_found(async_mpt_ops, invalid_module_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.accounts.modules.get(invalid_module_id)


async def test_filter_modules(async_mpt_ops, module_id, module_name):
    select_fields = ["-description"]
    filtered_modules = (
        async_mpt_ops.accounts.modules.filter(RQLQuery(id=module_id))
        .filter(RQLQuery(name=module_name))
        .select(*select_fields)
    )

    result = [filtered_module async for filtered_module in filtered_modules.iterate()]

    assert len(result) == 1

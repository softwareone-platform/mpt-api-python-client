import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery


def test_get_module_by_id(mpt_ops, module_id):
    result = mpt_ops.accounts.modules.get(module_id)

    assert result is not None


def test_list_modules(mpt_ops):
    limit = 10

    result = mpt_ops.accounts.modules.fetch_page(limit=limit)

    assert len(result) > 0


def test_get_module_by_id_not_found(mpt_ops, invalid_module_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_ops.accounts.modules.get(invalid_module_id)


def test_filter_modules(mpt_ops, module_id, module_name):
    select_fields = ["-description"]
    filtered_modules = (
        mpt_ops.accounts.modules
        .filter(RQLQuery(id=module_id))
        .filter(RQLQuery(name=module_name))
        .select(*select_fields)
    )

    result = list(filtered_modules.iterate())

    assert len(result) == 1

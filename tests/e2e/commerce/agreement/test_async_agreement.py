import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def created_agreement(async_mpt_ops, agreement_factory):
    new_agreement_request_data = agreement_factory(
        name="E2E Created Agreement",
    )

    return await async_mpt_ops.commerce.agreements.create(new_agreement_request_data)


async def test_get_agreement_by_id(async_mpt_ops, agreement_id):
    result = await async_mpt_ops.commerce.agreements.get(agreement_id)

    assert result is not None


async def test_list_agreements(async_mpt_ops):
    limit = 10

    result = await async_mpt_ops.commerce.agreements.fetch_page(limit=limit)

    assert len(result) > 0


async def test_get_agreement_by_id_not_found(async_mpt_ops, invalid_agreement_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_mpt_ops.commerce.agreements.get(invalid_agreement_id)


async def test_filter_agreements(async_mpt_ops, agreement_id):
    select_fields = ["-value"]
    filtered_agreements = (
        async_mpt_ops.commerce.agreements.filter(RQLQuery(id=agreement_id))
        .filter(RQLQuery(name="E2E Seeded For Commerce for Test Api Client Client"))
        .select(*select_fields)
    )

    result = [filtered_agreement async for filtered_agreement in filtered_agreements.iterate()]

    assert len(result) == 1


def test_create_agreement(created_agreement):
    result = created_agreement

    assert result is not None


async def test_update_agreement(async_mpt_ops, created_agreement, agreement_factory):
    updated_name = "E2E Updated Agreement Name"
    updated_agreement_data = agreement_factory(name=updated_name)

    result = await async_mpt_ops.commerce.agreements.update(
        created_agreement.id, updated_agreement_data
    )

    assert result is not None


async def test_get_agreement_render(async_mpt_ops, agreement_id):
    result = await async_mpt_ops.commerce.agreements.render(agreement_id)

    assert result is not None


async def test_get_agreement_template(async_mpt_ops, agreement_id):
    result = await async_mpt_ops.commerce.agreements.template(agreement_id)

    assert result is not None

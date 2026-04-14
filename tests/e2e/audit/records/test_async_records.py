from typing import Any

import pytest

from mpt_api_client import AsyncMPTClient
from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.audit.records import Record
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
async def created_record(async_mpt_vendor: AsyncMPTClient, record_data: dict[str, Any]) -> Record:
    service = async_mpt_vendor.audit.records
    return await service.create(record_data)


def test_create_record(created_record: Record, record_data: dict[str, Any]) -> None:  # noqa: AAA01
    assert created_record.event == record_data["event"]
    assert created_record.object.id == record_data["object"]["id"]


async def test_get_record(async_mpt_vendor: AsyncMPTClient, audit_record_id: str) -> None:
    service = async_mpt_vendor.audit.records
    result = await service.get(audit_record_id)

    assert result.id == audit_record_id


async def test_iterate_records(async_mpt_vendor: AsyncMPTClient, product_id: str) -> None:
    service = async_mpt_vendor.audit.records.filter(RQLQuery(object__id=product_id))
    records = [record async for record in service.iterate()]

    result = records[0]

    assert result.object.id == product_id


async def test_get_record_not_found(async_mpt_vendor: AsyncMPTClient) -> None:
    service = async_mpt_vendor.audit.records

    with pytest.raises(MPTAPIError):
        await service.get("REC-000-000-000")


async def test_get_records_with_render(async_mpt_vendor: AsyncMPTClient, product_id: str) -> None:
    template_chars = ["{{", "}}"]
    audit_filter = RQLQuery(object__id=product_id)
    service = async_mpt_vendor.audit.records.filter(audit_filter).options(render=True)
    records = [record async for record in service.iterate()]

    assert records
    for record in records:
        assert record.object.id == product_id
        assert not any(char in record.details for char in template_chars)


async def test_get_record_with_render(
    async_mpt_vendor: AsyncMPTClient, audit_record_id: str
) -> None:
    template_chars = ["{{", "}}"]
    service = async_mpt_vendor.audit.records.options(render=True)

    result = await service.get(audit_record_id)

    assert result.id == audit_record_id
    assert not any(char in result.details for char in template_chars)


async def test_get_record_with_select(
    async_mpt_vendor: AsyncMPTClient, audit_record_id: str
) -> None:
    service = async_mpt_vendor.audit.records

    result = await service.get(audit_record_id, select=["object", "actor"])

    assert result.id == audit_record_id
    assert result.object is not None
    assert result.actor is not None


async def test_get_record_with_render_and_select(
    async_mpt_vendor: AsyncMPTClient, audit_record_id: str
) -> None:
    template_chars = ["{{", "}}"]
    service = async_mpt_vendor.audit.records.options(render=True)

    result = await service.get(audit_record_id, select=["object", "actor", "details"])

    assert result.id == audit_record_id
    assert result.object is not None
    assert not any(char in result.details for char in template_chars)

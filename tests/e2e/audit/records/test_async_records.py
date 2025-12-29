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

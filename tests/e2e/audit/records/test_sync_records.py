from typing import Any

import pytest

from mpt_api_client import MPTClient
from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.audit.records import Record
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_record(mpt_vendor: MPTClient, record_data: dict[str, Any]) -> Record:
    service = mpt_vendor.audit.records
    return service.create(record_data)


def test_create_record(created_record: Record, record_data: dict[str, Any]) -> None:  # noqa: AAA01
    assert created_record.event == record_data["event"]
    assert created_record.object.id == record_data["object"]["id"]


def test_get_record(mpt_vendor: MPTClient, audit_record_id) -> None:
    service = mpt_vendor.audit.records

    result = service.get(audit_record_id)

    assert result.id == audit_record_id


def test_iterate_records(mpt_vendor: MPTClient, product_id) -> None:
    service = mpt_vendor.audit.records.filter(RQLQuery(object__id=product_id))
    records = list(service.iterate())

    result = records[0]

    assert result.object.id == product_id


def test_get_record_not_found(mpt_vendor: MPTClient) -> None:
    service = mpt_vendor.audit.records

    with pytest.raises(MPTAPIError):
        service.get("REC-000-000-000")

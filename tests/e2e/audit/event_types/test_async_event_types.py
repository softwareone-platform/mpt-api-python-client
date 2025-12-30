from typing import Any

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.audit.event_types import AsyncEventTypesService, EventType
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


async def test_get_event_type(
    async_event_types_service: AsyncEventTypesService, event_type: EventType
) -> None:
    result = await async_event_types_service.get(event_type.id)

    assert result.id == event_type.id
    assert result.key == event_type.key


async def test_filter_event_types(
    async_event_types_service: AsyncEventTypesService, event_type: EventType
) -> None:
    iterator = async_event_types_service.filter(RQLQuery(id=event_type.id)).iterate()

    result = [event_type_item async for event_type_item in iterator]

    assert len(result) == 1
    assert result[0].id == event_type.id


async def test_update_event_type(
    async_event_types_service: AsyncEventTypesService,
    event_type: EventType,
    event_type_update_data: dict[str, Any],
) -> None:
    result = await async_event_types_service.update(event_type.id, event_type_update_data)

    assert result.id == event_type.id


async def test_get_event_type_not_found(async_event_types_service: AsyncEventTypesService) -> None:
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        await async_event_types_service.get("EVT-000-000")

from typing import Any

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.resources.audit.event_types import EventType, EventTypesService
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


def test_get_event_type(event_types_service: EventTypesService, event_type: EventType) -> None:
    result = event_types_service.get(event_type.id)

    assert result.id == event_type.id
    assert result.key == event_type.key


def test_filter_event_types(event_types_service: EventTypesService, event_type: EventType) -> None:
    result = list(event_types_service.filter(RQLQuery(id=event_type.id)).iterate())

    assert len(result) == 1
    assert result[0].id == event_type.id


def test_update_event_type(
    event_types_service: EventTypesService,
    event_type: EventType,
    event_type_update_data: dict[str, Any],
) -> None:
    result = event_types_service.update(event_type.id, event_type_update_data)

    assert result.id == event_type.id


def test_get_event_type_not_found(event_types_service: EventTypesService) -> None:
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        event_types_service.get("EVT-000-000")

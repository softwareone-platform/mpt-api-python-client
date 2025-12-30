from typing import Any

import pytest

from mpt_api_client import AsyncMPTClient, MPTClient
from mpt_api_client.resources.audit.event_types import (
    AsyncEventTypesService,
    EventType,
    EventTypesService,
)


@pytest.fixture
def event_types_service(mpt_vendor: MPTClient) -> EventTypesService:
    return mpt_vendor.audit.event_types


@pytest.fixture
def async_event_types_service(async_mpt_vendor: AsyncMPTClient) -> AsyncEventTypesService:
    return async_mpt_vendor.audit.event_types


@pytest.fixture
def event_type(event_types_service: EventTypesService) -> EventType:
    return next(event_types_service.iterate())


@pytest.fixture
def event_type_update_data() -> dict[str, Any]:
    return {
        "description": "Updated description for e2e testing",
    }

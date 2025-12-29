from typing import Any

import pytest


@pytest.fixture
def record_data(account_id: str) -> dict[str, Any]:
    return {
        "event": "extensions.e2e.test",
        "object": {"id": account_id, "name": "e2e test account"},
        "details": "e2e test details",
        "summary": "e2e test summary",
        "actor": {
            "type": "system",
            "id": "system",
        },
        "payload": {
            "key": "value",
        },
    }


@pytest.fixture
def audit_record_id(e2e_config):
    return e2e_config["audit.record.id"]

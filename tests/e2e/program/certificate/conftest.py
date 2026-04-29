import pytest


@pytest.fixture
def invalid_certificate_id():
    return "CER-0000-0000-0000"


@pytest.fixture
def certificate_data(program_id, licensee_id, buyer_account_id):
    return {
        "name": "E2E Created Program Certificate",
        "program": {"id": program_id},
        "licensee": {"id": licensee_id},
        "client": {"id": buyer_account_id},
        "parameters": {"ordering": [], "fulfillment": []},
    }


@pytest.fixture
def terminated_certificate_data_factory():
    def factory(certificate_id: str):
        return {
            "id": certificate_id,
            "status": "terminated",
            "statusNotes": {
                "message": "Terminating certificate for E2E test",
            },
        }

    return factory

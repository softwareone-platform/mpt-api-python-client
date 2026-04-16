import pytest


@pytest.fixture
def program_data():
    return {
        "name": "E2E Created Program",
        "website": "www.example.com",
        "eligibility": {"client": True, "partner": True},
        "applicableTo": "Licensee",
    }


@pytest.fixture
def invalid_program_id():
    return "PRG-0000-0000"

import pytest

from mpt_api_client.resources.program.program import AsyncProgram, Program
from mpt_api_client.resources.program.programs import AsyncProgramsService, ProgramsService


@pytest.fixture
def program(http_client):
    return Program(http_client=http_client)


@pytest.fixture
def async_program(async_http_client):
    return AsyncProgram(http_client=async_http_client)


@pytest.mark.parametrize(
    ("property_name", "expected_service_class"),
    [
        ("programs", ProgramsService),
    ],
)
def test_program_properties(program, property_name, expected_service_class):
    result = getattr(program, property_name)

    assert isinstance(result, expected_service_class)
    assert result.http_client is program.http_client


@pytest.mark.parametrize(
    ("property_name", "expected_service_class"),
    [
        ("programs", AsyncProgramsService),
    ],
)
def test_async_program_properties(async_program, property_name, expected_service_class):
    result = getattr(async_program, property_name)

    assert isinstance(result, expected_service_class)
    assert result.http_client is async_program.http_client


def test_program_initialization(http_client):
    result = Program(http_client=http_client)

    assert result.http_client is http_client
    assert isinstance(result, Program)


def test_async_program_initialization(async_http_client):
    result = AsyncProgram(http_client=async_http_client)

    assert result.http_client is async_http_client
    assert isinstance(result, AsyncProgram)

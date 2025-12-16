import pytest

from tests.e2e.helper import (
    async_create_fixture_resource_and_delete,
    create_fixture_resource_and_delete,
)


@pytest.fixture
def contact_data(short_uuid):
    return {
        "name": "E2E delete me",
        "firstName": "Will",
        "lastName": "Smith",
        "email": f"{short_uuid}@example.com",
        "optOuts": [],
    }


@pytest.fixture
def created_contact(mpt_ops, contact_data):
    service = mpt_ops.notifications.contacts
    with create_fixture_resource_and_delete(service, contact_data) as contact:
        yield contact


@pytest.fixture
async def async_created_contact(async_mpt_ops, contact_data):
    service = async_mpt_ops.notifications.contacts
    async with async_create_fixture_resource_and_delete(service, contact_data) as contact:
        yield contact


@pytest.fixture
def created_contact_id(created_contact):
    return created_contact.id


@pytest.fixture
def invalid_contact_id():
    return "CON-0000-0000-0000"

import pytest

from mpt_api_client import RQLQuery
from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


def test_created_contact(created_contact):  # noqa: AAA01
    assert created_contact is not None


def test_get_contact(mpt_ops, created_contact_id):
    service = mpt_ops.notifications.contacts

    result = service.get(created_contact_id)

    assert result.id == created_contact_id


def test_list_contacts(mpt_ops, created_contact_id):
    iterator = mpt_ops.notifications.contacts.filter(RQLQuery(id=created_contact_id)).iterate()

    result = list(iterator)

    assert len(result) == 1
    assert result[0].id == created_contact_id


def test_get_contact_not_found(mpt_ops, invalid_contact_id):
    service = mpt_ops.notifications.contacts

    with pytest.raises(MPTAPIError):
        service.get(invalid_contact_id)


def test_block_unblock_contact(mpt_ops, created_contact):  # noqa: AAA01
    service = mpt_ops.notifications.contacts

    result_block = service.block(created_contact.id)
    result_unblock = service.unblock(created_contact.id)

    assert result_block.status == "Blocked"
    assert result_unblock.status == "Active"


def test_update_contact(mpt_ops, created_contact, short_uuid):
    service = mpt_ops.notifications.contacts
    new_name = f"delete {short_uuid}"

    result = service.update(
        created_contact.id,
        {
            "name": new_name,
        },
    )

    assert result.name == new_name


def test_delete_contact(mpt_ops, created_contact_id):
    service = mpt_ops.notifications.contacts

    service.delete(created_contact_id)  # act

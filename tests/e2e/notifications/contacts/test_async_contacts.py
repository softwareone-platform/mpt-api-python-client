import pytest

from mpt_api_client import RQLQuery
from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


def test_create_contact(created_contact):  # noqa: AAA01
    assert created_contact is not None


async def test_get_contact(async_mpt_ops, created_contact_id):
    result = await async_mpt_ops.notifications.contacts.get(created_contact_id)

    assert result.id == created_contact_id


async def test_list_contacts(async_mpt_ops, created_contact_id):
    iterator = async_mpt_ops.notifications.contacts.filter(
        RQLQuery(id=created_contact_id)
    ).iterate()

    result = [contact async for contact in iterator]

    assert len(result) == 1
    assert result[0].id == created_contact_id


async def test_get_contact_not_found(async_mpt_ops):
    service = async_mpt_ops.notifications.contacts

    with pytest.raises(MPTAPIError):
        await service.get("CON-0000-0000-0000")


async def test_block_unblock_contact(async_mpt_ops, created_contact):
    service = async_mpt_ops.notifications.contacts

    result_block = await service.block(created_contact.id)
    result_unblock = await service.unblock(created_contact.id)

    assert result_block.status == "Blocked"
    assert result_unblock.status == "Active"


async def test_update_contact(async_mpt_ops, created_contact, short_uuid):
    service = async_mpt_ops.notifications.contacts
    new_name = f"delete {short_uuid}"
    result = await service.update(
        created_contact.id,
        {
            "name": new_name,
        },
    )

    assert result.name == new_name


async def test_delete_contact(async_mpt_ops, created_contact):
    service = async_mpt_ops.notifications.contacts

    await service.delete(created_contact.id)

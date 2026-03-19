import pytest

from mpt_api_client.exceptions import MPTAPIError

pytestmark = [pytest.mark.flaky]


def test_list_chat_links(chat_links_service):
    result = chat_links_service.fetch_page(limit=1)

    assert len(result) > 0


def test_create_chat_link(created_chat_link, chat_link_data):  # noqa: AAA01
    assert created_chat_link.id is not None
    assert created_chat_link.to_dict().get("uri") == chat_link_data["uri"]


def test_update_chat_link_name(chat_links_service, created_chat_link, short_uuid):
    new_name = f"e2e updated link - {short_uuid}"

    result = chat_links_service.update(created_chat_link.id, {"name": new_name})

    assert result.id == created_chat_link.id
    assert result.to_dict().get("name") == new_name


def test_delete_chat_link(chat_links_service, created_chat_link):
    result = created_chat_link

    chat_links_service.delete(result.id)


def test_update_chat_link_not_found(chat_links_service, invalid_chat_link_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        chat_links_service.update(invalid_chat_link_id, {"name": "updated name"})


def test_delete_chat_link_not_found(chat_links_service, invalid_chat_link_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        chat_links_service.delete(invalid_chat_link_id)

import pytest

from mpt_api_client.exceptions import MPTAPIError
from tests.e2e.helper import assert_service_filter_with_iterate, assert_update_resource

pytestmark = [pytest.mark.flaky]


def test_create_footer(created_footer, footer_data):
    result = created_footer.content

    assert result == footer_data["content"]


def test_get_footer(footers_service, created_footer):
    result = footers_service.get(created_footer.id)

    assert result.id == created_footer.id


def test_get_footer_not_found(footers_service):
    bogus_id = "FLV-0000-0000"

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        footers_service.get(bogus_id)


def test_update_footer(footers_service, created_footer, short_uuid):
    new_content = f"e2e footer updated {short_uuid}"

    assert_update_resource(footers_service, created_footer.id, "content", new_content)  # act


def test_delete_footer(footers_service, created_footer):
    footers_service.delete(created_footer.id)

    result = footers_service.get(created_footer.id)

    assert result.status == "Deleted"


def test_delete_footer_not_found(footers_service):
    bogus_id = "FLV-0000-0000"

    with pytest.raises(MPTAPIError):
        footers_service.delete(bogus_id)


def test_filter_footers(footers_service, created_footer):
    assert_service_filter_with_iterate(footers_service, created_footer.id, None)  # act

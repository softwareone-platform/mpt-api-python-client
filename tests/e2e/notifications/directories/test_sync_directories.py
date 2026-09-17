import pytest

from mpt_api_client.exceptions import MPTAPIError
from tests.e2e.helper import assert_service_filter_with_iterate

pytestmark = [pytest.mark.flaky]


def test_get_directory(directories_service, directory_id):
    result = directories_service.get(directory_id)

    assert result.id == directory_id


def test_get_directory_not_found(directories_service):
    bogus_id = "DIR-0000-0000"

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        directories_service.get(bogus_id)


def test_filter_directories(directories_service, directory_id):
    assert_service_filter_with_iterate(directories_service, directory_id, None)  # act

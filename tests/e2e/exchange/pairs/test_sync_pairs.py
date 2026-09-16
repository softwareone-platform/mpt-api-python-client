import pytest

from mpt_api_client.exceptions import MPTAPIError
from tests.e2e.helper import assert_service_filter_with_iterate

pytestmark = [pytest.mark.flaky]


def test_get_pair(pairs_service, pair_id):
    result = pairs_service.get(pair_id)

    assert result.id == pair_id


def test_get_pair_not_found(pairs_service):
    bogus_id = "FXP-0000-0000"

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        pairs_service.get(bogus_id)


def test_filter_pairs(pairs_service, pair_id):
    assert_service_filter_with_iterate(pairs_service, pair_id, None)  # act

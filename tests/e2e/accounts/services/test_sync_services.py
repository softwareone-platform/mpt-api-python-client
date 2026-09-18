import pytest

from mpt_api_client.exceptions import MPTAPIError
from tests.e2e.helper import assert_service_filter_with_iterate

pytestmark = [pytest.mark.flaky]


def test_get_service(services_service, service_id):
    result = services_service.get(service_id)

    assert result.id == service_id


def test_get_service_not_found(services_service, invalid_service_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        services_service.get(invalid_service_id)


def test_list_services(services_service):
    limit = 10

    result = services_service.fetch_page(limit=limit)

    assert len(result) > 0


def test_filter_services(services_service, service_id):
    assert_service_filter_with_iterate(services_service, service_id, None)  # act

import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


def test_create_pricing_policy(created_pricing_policy, pricing_policy_data):
    result = created_pricing_policy

    assert result.name == pricing_policy_data["name"]


def test_get_pricing_policy(pricing_policies_service, created_pricing_policy):
    result = pricing_policies_service.get(created_pricing_policy.id)

    assert result.id == created_pricing_policy.id


def test_get_pricing_policy_by_id(pricing_policies_service, pricing_policy_id):
    result = pricing_policies_service.get(pricing_policy_id)

    assert result.id == pricing_policy_id


def test_iterate_pricing_policies(pricing_policies_service, created_pricing_policy):
    policies = list(pricing_policies_service.iterate())

    result = any(policy.id == created_pricing_policy.id for policy in policies)

    assert result is True


def test_filter_pricing_policies(pricing_policies_service, created_pricing_policy):
    target_id = created_pricing_policy.id
    select_fields = ["-description"]
    filtered = pricing_policies_service.filter(RQLQuery(id=target_id)).select(*select_fields)

    result = list(filtered.iterate())

    assert len(result) == 1
    assert result[0].id == target_id


def test_activate_deactivate_pricing_policy(pricing_policies_service, created_pricing_policy):  # noqa: AAA01
    deactivate = pricing_policies_service.disable(created_pricing_policy.id)
    assert deactivate.id == created_pricing_policy.id

    activated = pricing_policies_service.activate(deactivate.id)
    assert activated.id == created_pricing_policy.id


def test_delete_pricing_policy(pricing_policies_service, created_pricing_policy):
    pricing_policies_service.delete(created_pricing_policy.id)  # act


def test_get_pricing_policy_not_found(pricing_policies_service):
    bogus_id = "PPY-0000-NOTFOUND"

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        pricing_policies_service.get(bogus_id)


def test_create_pricing_policy_invalid_data(pricing_policies_service):
    invalid_data = {"name": "e2e - delete me", "description": "invalid data"}

    with pytest.raises(MPTAPIError, match=r"400 One or more validation errors occurred"):
        pricing_policies_service.create(invalid_data)

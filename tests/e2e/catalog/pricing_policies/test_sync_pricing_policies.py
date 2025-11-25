import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def pricing_policies_service(mpt_ops):
    return mpt_ops.catalog.pricing_policies


@pytest.fixture
def created_pricing_policy(pricing_policies_service, pricing_policy_data):
    policy = pricing_policies_service.create(pricing_policy_data)

    yield policy

    try:
        pricing_policies_service.delete(policy.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete pricing policy {policy.id}: {error.title}")


def test_create_pricing_policy(created_pricing_policy, pricing_policy_data):
    assert created_pricing_policy.name == pricing_policy_data["name"]


def test_get_pricing_policy(pricing_policies_service, created_pricing_policy):
    fetched = pricing_policies_service.get(created_pricing_policy.id)
    assert fetched.id == created_pricing_policy.id


def test_get_pricing_policy_by_id(pricing_policies_service, pricing_policy_id):
    if not pricing_policy_id:
        pytest.skip("No pricing_policy_id configured")
    fetched = pricing_policies_service.get(pricing_policy_id)
    assert fetched.id == pricing_policy_id


def test_iterate_pricing_policies(pricing_policies_service, created_pricing_policy):
    policies = list(pricing_policies_service.iterate())
    assert any(policy.id == created_pricing_policy.id for policy in policies)


def test_filter_pricing_policies(pricing_policies_service, created_pricing_policy):
    target_id = created_pricing_policy.id
    select_fields = ["-description"]
    filtered = pricing_policies_service.filter(RQLQuery(id=target_id)).select(*select_fields)
    policies = list(filtered.iterate())
    assert len(policies) == 1
    assert policies[0].id == target_id


def test_activate_deactivate_pricing_policy(pricing_policies_service, created_pricing_policy):
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

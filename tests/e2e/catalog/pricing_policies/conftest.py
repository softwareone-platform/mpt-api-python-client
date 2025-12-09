import pytest

from mpt_api_client.exceptions import MPTAPIError


@pytest.fixture
def pricing_policy_data(client_account_id, product_id):
    return {
        "name": "e2e - pricing policy please delete",
        "description": "Test pricing policy description",
        "client": {"id": client_account_id},
        "product": {"id": product_id},
        "eligibility": {"client": True, "partner": False},
        "margin": "0.20",
    }


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


@pytest.fixture
def pricing_policy_id(created_pricing_policy):
    return created_pricing_policy.id

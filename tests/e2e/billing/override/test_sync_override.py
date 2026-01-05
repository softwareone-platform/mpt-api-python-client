import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


def test_get_billing_override_by_id(mpt_ops, billing_override_id):
    result = mpt_ops.billing.manual_overrides.get(billing_override_id)

    assert result is not None


def test_list_billing_overrides(mpt_ops):
    limit = 10

    result = mpt_ops.billing.manual_overrides.fetch_page(limit=limit)

    assert len(result) > 0


def test_get_billing_override_by_id_not_found(mpt_ops, invalid_billing_override_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_ops.billing.manual_overrides.get(invalid_billing_override_id)


def test_filter_billing_overrides(mpt_ops, billing_override_id):
    select_fields = ["-client"]
    filtered_billing_overrides = (
        mpt_ops.billing.manual_overrides.filter(RQLQuery(id=billing_override_id))
        .filter(RQLQuery(externalId="e2e-seeded-override"))
        .select(*select_fields)
    )

    result = list(filtered_billing_overrides.iterate())

    assert len(result) == 1

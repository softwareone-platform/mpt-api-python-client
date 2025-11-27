import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_agreement(mpt_ops, agreement_factory, logger):
    new_agreement_request_data = agreement_factory(
        name="E2E Created Agreement",
    )

    new_agreement = mpt_ops.commerce.agreements.create(new_agreement_request_data)

    yield new_agreement

    try:
        mpt_ops.commerce.agreements.delete(new_agreement.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete agreement: {error.title}")  # noqa: WPS421


def test_get_agreement_by_id(mpt_ops, agreement_id):
    agreement = mpt_ops.commerce.agreements.get(agreement_id)
    assert agreement is not None


def test_list_agreements(mpt_ops):
    limit = 10
    agreements = mpt_ops.commerce.agreements.fetch_page(limit=limit)
    assert len(agreements) > 0


def test_get_agreement_by_id_not_found(mpt_ops, invalid_agreement_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_ops.commerce.agreements.get(invalid_agreement_id)


def test_filter_agreements(mpt_ops, agreement_id):
    select_fields = ["-value"]

    filtered_agreements = (
        mpt_ops.commerce.agreements.filter(RQLQuery(id=agreement_id))
        .filter(RQLQuery(name="E2E Seeded Agreement"))
        .select(*select_fields)
    )

    agreements = list(filtered_agreements.iterate())

    assert len(agreements) == 1


def test_create_agreement(created_agreement):
    new_agreement = created_agreement
    assert new_agreement is not None


def test_update_agreement(mpt_ops, created_agreement, agreement_factory):
    updated_name = "E2E Updated Agreement Name"
    updated_agreement_data = agreement_factory(name=updated_name)

    updated_agreement = mpt_ops.commerce.agreements.update(
        created_agreement.id, updated_agreement_data
    )

    assert updated_agreement is not None


def test_get_agreement_render(mpt_ops, agreement_id):
    rendered_agreement = mpt_ops.commerce.agreements.render(agreement_id)
    assert rendered_agreement is not None


def test_get_agreement_template(mpt_ops, agreement_id):
    template = mpt_ops.commerce.agreements.template(agreement_id)
    assert template is not None

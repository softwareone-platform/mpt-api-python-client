import pytest

from mpt_api_client.exceptions import MPTAPIError
from mpt_api_client.rql.query_builder import RQLQuery

pytestmark = [pytest.mark.flaky]


@pytest.fixture
def created_licensee(mpt_client, licensee_factory, account_icon):
    new_licensee_request_data = licensee_factory(name="E2E Created licensee")

    new_licensee = mpt_client.accounts.licensees.create(
        new_licensee_request_data, logo=account_icon
    )

    yield new_licensee

    try:
        mpt_client.accounts.licensees.delete(new_licensee.id)
    except MPTAPIError as error:
        print(f"TEARDOWN - Unable to delete licensee: {error.title}")  # noqa: WPS421


def test_get_licensee_by_id(mpt_client, licensee_id):
    result = mpt_client.accounts.licensees.get(licensee_id)

    assert result is not None


def test_list_licensees(mpt_client):
    limit = 10

    result = mpt_client.accounts.licensees.fetch_page(limit=limit)

    assert len(result) > 0


def test_get_licensee_by_id_not_found(mpt_client, invalid_licensee_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_client.accounts.licensees.get(invalid_licensee_id)


def test_filter_licensees(mpt_client, licensee_id):
    select_fields = ["-address"]
    filtered_licensees = (
        mpt_client.accounts.licensees.filter(RQLQuery(id=licensee_id))
        .filter(RQLQuery(name="E2E Seeded Licensee"))
        .select(*select_fields)
    )

    result = list(filtered_licensees.iterate())

    assert len(result) == 1


def test_create_licensee(created_licensee):
    result = created_licensee

    assert result is not None


def test_delete_licensee(mpt_client, created_licensee):
    mpt_client.accounts.licensees.delete(created_licensee.id)  # act


def test_delete_licensee_not_found(mpt_client, invalid_licensee_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_client.accounts.licensees.delete(invalid_licensee_id)


def test_update_licensee(mpt_client, licensee_factory, account_icon, created_licensee):
    updated_licensee_data = licensee_factory(name="E2E Updated Licensee")

    result = mpt_client.accounts.licensees.update(
        created_licensee.id, updated_licensee_data, logo=account_icon
    )

    assert result is not None


def test_update_licensee_not_found(mpt_client, licensee_factory, account_icon, invalid_licensee_id):
    updated_licensee_data = licensee_factory(name="Nonexistent Licensee")

    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_client.accounts.licensees.update(
            invalid_licensee_id, updated_licensee_data, logo=account_icon
        )


def test_licensee_disable(mpt_client, created_licensee):
    result = mpt_client.accounts.licensees.disable(created_licensee.id)

    assert result is not None


def test_licensee_disable_not_found(mpt_client, invalid_licensee_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_client.accounts.licensees.disable(invalid_licensee_id)


def test_licensee_enable(mpt_client, created_licensee):
    mpt_client.accounts.licensees.disable(created_licensee.id)

    result = mpt_client.accounts.licensees.enable(created_licensee.id)

    assert result is not None


def test_licensee_enable_not_found(mpt_client, invalid_licensee_id):
    with pytest.raises(MPTAPIError, match=r"404 Not Found"):
        mpt_client.accounts.licensees.enable(invalid_licensee_id)
